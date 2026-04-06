import calendar
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException

from app.enums import (
    DependencyStatus,
    Recurrence,
    RecurrenceUnit,
    SortBy,
    SortOrder,
    TodoHistoryChangeBy,
    TodoStatus,
)
from app.models.todo import Todo
from app.repository.dependency_repo import DependencyRepository
from app.repository.history_repo import HistoryRepository
from app.repository.todo_repo import TodoRepository
from app.schemas.dependency import AddDependenciesRequest, DependencyMutationResult
from app.schemas.history import TodoHistoryResponse
from app.schemas.search import TodoSearchResponse
from app.schemas.subgraph import SubgraphEdge, TodoSubgraph
from app.schemas.todo import RecurrenceSchema, TodoCreate, TodoResponse, TodoUpdate


def _add_months(dt: datetime, months: int) -> datetime:
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def _get_next_due_date(base_date: datetime, recurrence: dict) -> datetime:
    from datetime import timedelta

    rec_type = recurrence.get("type")
    if rec_type == Recurrence.DAILY:
        return base_date + timedelta(days=1)
    if rec_type == Recurrence.WEEKLY:
        return base_date + timedelta(weeks=1)
    if rec_type == Recurrence.MONTHLY:
        return _add_months(base_date, 1)
    if rec_type == Recurrence.CUSTOM:
        interval = int(recurrence.get("interval", 1))
        unit = recurrence.get("unit")
        if unit == RecurrenceUnit.WEEK:
            return base_date + timedelta(weeks=interval)
        if unit == RecurrenceUnit.MONTH:
            return _add_months(base_date, interval)
        return base_date + timedelta(days=interval)
    return base_date


def _normalize_recurrence(recurrence: RecurrenceSchema) -> dict:
    if recurrence.type != Recurrence.CUSTOM:
        return {"type": recurrence.type.value}
    if not recurrence.interval or not recurrence.unit:
        raise HTTPException(
            status_code=400,
            detail="Custom recurrence requires both interval and unit",
        )
    return {
        "type": recurrence.type.value,
        "interval": recurrence.interval,
        "unit": recurrence.unit.value,
    }


class TodoService:
    def __init__(
        self,
        todo_repo: TodoRepository,
        dep_repo: DependencyRepository,
        history_repo: HistoryRepository,
    ) -> None:
        self.todo_repo = todo_repo
        self.dep_repo = dep_repo
        self.history_repo = history_repo

    # ------------------------------------------------------------------ #
    # CRUD
    # ------------------------------------------------------------------ #

    async def create(self, data: TodoCreate) -> TodoResponse:
        self._assert_due_date_for_recurrence(data.due_date, data.recurrence)
        payload = data.model_dump(exclude_none=True, by_alias=False)
        if data.recurrence:
            payload["recurrence"] = _normalize_recurrence(data.recurrence)
        todo = await self.todo_repo.create(payload)
        return TodoResponse.model_validate(todo)

    async def find_one(self, id: UUID) -> TodoResponse:
        todo = await self._get_or_404(id)
        return TodoResponse.model_validate(todo)

    async def update(self, id: UUID, data: TodoUpdate) -> TodoResponse:
        todo = await self._get_or_404(id)

        # Determine next values for validation (only for fields that were sent)
        fields_set = data.model_fields_set
        next_status = data.status if "status" in fields_set else todo.status
        next_due_date = data.due_date if "due_date" in fields_set else todo.due_date
        next_recurrence = data.recurrence if "recurrence" in fields_set else (
            RecurrenceSchema(**todo.recurrence) if todo.recurrence else None
        )

        self._assert_due_date_for_recurrence(next_due_date, next_recurrence)

        if todo.status != TodoStatus.IN_PROGRESS and next_status == TodoStatus.IN_PROGRESS:
            await self._ensure_dependencies_ready(id)

        update_payload = self._build_update_payload(data)
        old_status = todo.status
        updated = await self.todo_repo.update(todo, update_payload)

        if old_status != updated.status:
            await self.history_repo.create(
                todo_id=id,
                from_status=old_status,
                to_status=updated.status,
                changed_by=TodoHistoryChangeBy.MANUAL,
            )

        await self._handle_recurring_todo(id, old_status, updated)
        return TodoResponse.model_validate(updated)

    async def remove(self, id: UUID) -> TodoResponse:
        todo = await self._get_or_404(id)
        now = datetime.utcnow()
        await self.todo_repo.soft_delete(id, now)
        await self.dep_repo.soft_delete_edges_by_todo(id, now)
        return TodoResponse.model_validate(todo)

    # ------------------------------------------------------------------ #
    # Search
    # ------------------------------------------------------------------ #

    async def search(
        self,
        name: Optional[str],
        status: Optional[TodoStatus],
        priority,
        due_date_start: Optional[datetime],
        due_date_end: Optional[datetime],
        dependency_status: Optional[DependencyStatus],
        sort_by: SortBy,
        sort_order: SortOrder,
        page: int,
        limit: int,
    ) -> TodoSearchResponse:
        rows, total = await self.todo_repo.search(
            name=name,
            status=status,
            priority=priority,
            due_date_start=due_date_start,
            due_date_end=due_date_end,
            dependency_status=dependency_status,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            limit=limit,
        )
        results = []
        for todo, dep_status_val in rows:
            resp = TodoResponse.model_validate(todo)
            resp.dependency_status = DependencyStatus(dep_status_val)
            results.append(resp)

        return TodoSearchResponse(total=total, page=page, limit=limit, results=results)

    # ------------------------------------------------------------------ #
    # Dependencies
    # ------------------------------------------------------------------ #

    async def add_dependencies(
        self, dependent_id: UUID, body: AddDependenciesRequest
    ) -> DependencyMutationResult:
        prereq_ids = body.prerequisite_ids
        if not prereq_ids:
            return DependencyMutationResult(dependent_id=str(dependent_id), created=0)

        unique_ids = list(set(prereq_ids))

        if str(dependent_id) in unique_ids:
            raise HTTPException(status_code=400, detail="Todo cannot depend on itself")

        dependent = await self._get_or_404(dependent_id)

        prereq_uuids = [UUID(pid) for pid in unique_ids]
        prerequisites = await self.todo_repo.get_by_ids(prereq_uuids)
        found_ids = {str(p.id) for p in prerequisites}
        missing = [pid for pid in unique_ids if pid not in found_ids]
        if missing:
            raise HTTPException(
                status_code=404,
                detail=f"Prerequisite todo(s) not found: {', '.join(missing)}",
            )

        cycle_ids = await self.dep_repo.find_cycle_prerequisite_ids(prereq_uuids, dependent_id)
        if cycle_ids:
            prereq_map = {str(p.id): p.name for p in prerequisites}
            labels = [prereq_map.get(str(cid), str(cid)) for cid in cycle_ids]
            raise HTTPException(
                status_code=400,
                detail=f"Adding edge(s) {', '.join(labels)} -> {dependent.name} introduces a cycle",
            )

        existing = await self.dep_repo.get_existing_edges(dependent_id, prereq_uuids)
        existing_ids = {str(e.prerequisite_id) for e in existing}
        to_create = [uid for uid in prereq_uuids if str(uid) not in existing_ids]

        if to_create:
            await self.dep_repo.create_edges(dependent_id, to_create)

        return DependencyMutationResult(dependent_id=str(dependent_id), created=len(to_create))

    async def remove_dependencies(
        self, dependent_id: UUID, body: AddDependenciesRequest
    ) -> DependencyMutationResult:
        prereq_ids = body.prerequisite_ids
        if not prereq_ids:
            return DependencyMutationResult(dependent_id=str(dependent_id), removed=0)

        unique_ids = list(set(prereq_ids))
        prereq_uuids = [UUID(pid) for pid in unique_ids]
        removed = await self.dep_repo.soft_delete_edges(dependent_id, prereq_uuids)
        return DependencyMutationResult(dependent_id=str(dependent_id), removed=removed)

    async def list_dependencies(self, id: UUID) -> List[TodoResponse]:
        edges = await self.dep_repo.get_edges_by_dependent(id)
        if not edges:
            return []
        prereq_ids = list({e.prerequisite_id for e in edges})
        todos = await self.todo_repo.get_by_ids(prereq_ids)
        return [TodoResponse.model_validate(t) for t in todos]

    async def list_dependents(self, id: UUID) -> List[TodoResponse]:
        edges = await self.dep_repo.get_edges_by_prerequisite(id)
        if not edges:
            return []
        dep_ids = list({e.dependent_id for e in edges})
        todos = await self.todo_repo.get_by_ids(dep_ids)
        return [TodoResponse.model_validate(t) for t in todos]

    # ------------------------------------------------------------------ #
    # Subgraph
    # ------------------------------------------------------------------ #

    async def get_subgraph(self, id: UUID) -> TodoSubgraph:
        await self._get_or_404(id)

        raw_edges = await self.dep_repo.get_subgraph_raw(id)

        node_ids: set[UUID] = {id}
        seen: set[tuple] = set()
        edges: list[SubgraphEdge] = []

        for pre_str, dep_str in raw_edges:
            pre_id = UUID(pre_str)
            dep_id = UUID(dep_str)
            node_ids.add(pre_id)
            node_ids.add(dep_id)
            key = (pre_str, dep_str)
            if key not in seen:
                seen.add(key)
                edges.append(SubgraphEdge(prerequisite_id=pre_str, dependent_id=dep_str))

        todos = await self.todo_repo.get_by_ids(list(node_ids))
        nodes = [TodoResponse.model_validate(t) for t in todos]

        return TodoSubgraph(root_id=str(id), nodes=nodes, edges=edges)

    # ------------------------------------------------------------------ #
    # History
    # ------------------------------------------------------------------ #

    async def get_history(self, id: UUID) -> List[TodoHistoryResponse]:
        records = await self.history_repo.get_by_todo_id(id)
        return [TodoHistoryResponse.model_validate(r) for r in records]

    # ------------------------------------------------------------------ #
    # Private helpers
    # ------------------------------------------------------------------ #

    async def _get_or_404(self, id: UUID) -> Todo:
        todo = await self.todo_repo.get_by_id(id)
        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")
        return todo

    def _assert_due_date_for_recurrence(self, due_date, recurrence) -> None:
        if recurrence and not due_date:
            raise HTTPException(
                status_code=400,
                detail="Due date is required when recurrence is provided",
            )

    def _build_update_payload(self, data: TodoUpdate) -> dict:
        nullable_fields = {"description", "due_date", "recurrence"}
        payload: dict = {}

        for field in data.model_fields_set:
            value = getattr(data, field)
            if field in nullable_fields:
                if value is None:
                    payload[field] = None
                elif field == "recurrence":
                    payload[field] = _normalize_recurrence(value)
                else:
                    payload[field] = value
            elif value is not None:
                payload[field] = value

        return payload

    async def _handle_recurring_todo(self, todo_id: UUID, old_status: TodoStatus, updated: Todo) -> None:
        if (
            old_status == TodoStatus.COMPLETED
            or updated.status != TodoStatus.COMPLETED
            or not updated.recurrence
        ):
            return

        if updated.due_date:
            next_due_date = _get_next_due_date(updated.due_date, updated.recurrence)
            await self.todo_repo.update(
                updated,
                {"status": TodoStatus.NOT_STARTED, "due_date": next_due_date},
            )
            await self.history_repo.create(
                todo_id=todo_id,
                from_status=TodoStatus.COMPLETED,
                to_status=TodoStatus.NOT_STARTED,
                changed_by=TodoHistoryChangeBy.RECURRENCE,
            )

    async def _ensure_dependencies_ready(self, todo_id: UUID) -> None:
        edges = await self.dep_repo.get_edges_by_dependent(todo_id)
        if not edges:
            return

        prereq_ids = list({e.prerequisite_id for e in edges})
        prerequisites = await self.todo_repo.get_by_ids(prereq_ids)

        ready_statuses = {TodoStatus.COMPLETED, TodoStatus.ARCHIVED}
        blocked = [t for t in prerequisites if t.status not in ready_statuses]
        found_ids = {t.id for t in prerequisites}
        missing = [str(pid) for pid in prereq_ids if pid not in found_ids]

        if not blocked and not missing:
            return

        labels = [f"{t.name} ({t.status})" for t in blocked] + missing
        raise HTTPException(
            status_code=400,
            detail=(
                "Todo cannot move to IN_PROGRESS until dependencies are "
                f"COMPLETED or ARCHIVED: {', '.join(labels)}"
            ),
        )

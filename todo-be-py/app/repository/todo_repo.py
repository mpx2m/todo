import calendar
from datetime import datetime
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import case, func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import DependencyStatus, SortBy, SortOrder, TodoStatus
from app.models.todo import Todo
from app.models.todo_dependency import TodoDependency


# Map SortBy enum values to Todo column names
_SORT_FIELD_MAP = {
    SortBy.DUE_DATE: Todo.due_date,
    SortBy.PRIORITY: Todo.priority,
    SortBy.STATUS: Todo.status,
    SortBy.NAME: Todo.name,
}


class TodoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Optional[Todo]:
        result = await self.session.execute(
            select(Todo).where(Todo.id == id, Todo.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_by_ids(self, ids: List[UUID]) -> List[Todo]:
        if not ids:
            return []
        result = await self.session.execute(
            select(Todo).where(Todo.id.in_(ids), Todo.deleted_at.is_(None))
        )
        return list(result.scalars().all())

    async def create(self, data: dict) -> Todo:
        todo = Todo(**data)
        self.session.add(todo)
        await self.session.flush()
        await self.session.refresh(todo)
        return todo

    async def update(self, todo: Todo, data: dict) -> Todo:
        for key, value in data.items():
            setattr(todo, key, value)
        todo.updated_at = datetime.utcnow()
        self.session.add(todo)
        await self.session.flush()
        await self.session.refresh(todo)
        return todo

    async def soft_delete(self, id: UUID, now: datetime) -> None:
        await self.session.execute(
            update(Todo)
            .where(Todo.id == id, Todo.deleted_at.is_(None))
            .values(deleted_at=now)
        )

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
    ) -> Tuple[List[Tuple[Todo, str]], int]:
        # Correlated subquery: count blocking prerequisites
        blocking_count = (
            select(func.count())
            .select_from(TodoDependency)
            .join(Todo.__table__.alias("prereq"), text("prereq.id = todo_dependency.prerequisite_id"))
            .where(
                TodoDependency.dependent_id == Todo.id,
                TodoDependency.deleted_at.is_(None),
                text("prereq.deleted_at IS NULL"),
                text(f"prereq.status IN ('{TodoStatus.NOT_STARTED.value}', '{TodoStatus.IN_PROGRESS.value}')"),
            )
            .correlate(Todo)
            .scalar_subquery()
        )

        dep_status_expr = case(
            (blocking_count > 0, DependencyStatus.BLOCKED.value),
            else_=DependencyStatus.UNBLOCKED.value,
        ).label("dependency_status")

        conditions = [Todo.deleted_at.is_(None)]
        if status:
            conditions.append(Todo.status == status)
        if priority:
            conditions.append(Todo.priority == priority)
        if name and name.strip():
            conditions.append(Todo.name.ilike(f"%{name.strip()}%"))
        if due_date_start:
            conditions.append(Todo.due_date >= due_date_start)
        if due_date_end:
            conditions.append(Todo.due_date <= due_date_end)
        if dependency_status == DependencyStatus.BLOCKED:
            conditions.append(blocking_count > 0)
        elif dependency_status == DependencyStatus.UNBLOCKED:
            conditions.append(blocking_count == 0)

        count_stmt = select(func.count()).select_from(Todo).where(*conditions)
        total = (await self.session.execute(count_stmt)).scalar_one()

        sort_col = _SORT_FIELD_MAP.get(sort_by, Todo.due_date)
        order_expr = sort_col.asc() if sort_order == SortOrder.ASC else sort_col.desc()
        skip = (page - 1) * limit

        stmt = (
            select(Todo, dep_status_expr)
            .where(*conditions)
            .order_by(order_expr, Todo.id.desc())
            .offset(skip)
            .limit(limit)
        )
        rows = (await self.session.execute(stmt)).all()
        return list(rows), total

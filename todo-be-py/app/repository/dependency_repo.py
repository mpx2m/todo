from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo_dependency import TodoDependency


class DependencyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_edges_by_dependent(self, dependent_id: UUID) -> List[TodoDependency]:
        result = await self.session.execute(
            select(TodoDependency).where(
                TodoDependency.dependent_id == dependent_id,
                TodoDependency.deleted_at.is_(None),
            )
        )
        return list(result.scalars().all())

    async def get_edges_by_prerequisite(self, prerequisite_id: UUID) -> List[TodoDependency]:
        result = await self.session.execute(
            select(TodoDependency).where(
                TodoDependency.prerequisite_id == prerequisite_id,
                TodoDependency.deleted_at.is_(None),
            )
        )
        return list(result.scalars().all())

    async def get_existing_edges(self, dependent_id: UUID, prerequisite_ids: List[UUID]) -> List[TodoDependency]:
        if not prerequisite_ids:
            return []
        result = await self.session.execute(
            select(TodoDependency).where(
                TodoDependency.dependent_id == dependent_id,
                TodoDependency.prerequisite_id.in_(prerequisite_ids),
                TodoDependency.deleted_at.is_(None),
            )
        )
        return list(result.scalars().all())

    async def create_edges(self, dependent_id: UUID, prerequisite_ids: List[UUID]) -> int:
        edges = [
            TodoDependency(prerequisite_id=pid, dependent_id=dependent_id)
            for pid in prerequisite_ids
        ]
        self.session.add_all(edges)
        await self.session.flush()
        return len(edges)

    async def soft_delete_edges(self, dependent_id: UUID, prerequisite_ids: List[UUID]) -> int:
        if not prerequisite_ids:
            return 0
        result = await self.session.execute(
            update(TodoDependency)
            .where(
                TodoDependency.dependent_id == dependent_id,
                TodoDependency.prerequisite_id.in_(prerequisite_ids),
                TodoDependency.deleted_at.is_(None),
            )
            .values(deleted_at=datetime.utcnow())
        )
        return result.rowcount

    async def soft_delete_edges_by_todo(self, todo_id: UUID, now: datetime) -> None:
        await self.session.execute(
            update(TodoDependency)
            .where(
                TodoDependency.deleted_at.is_(None),
                (TodoDependency.prerequisite_id == todo_id) | (TodoDependency.dependent_id == todo_id),
            )
            .values(deleted_at=now)
        )

    async def find_cycle_prerequisite_ids(
        self, prerequisite_ids: List[UUID], dependent_id: UUID
    ) -> List[UUID]:
        """
        Use a recursive CTE to find all nodes downstream of `dependent_id`.
        Any proposed prerequisite that is downstream would create a cycle.
        """
        if not prerequisite_ids:
            return []

        prereq_strs = [str(pid) for pid in prerequisite_ids]

        sql = text("""
            WITH RECURSIVE downstream AS (
                SELECT td.dependent_id AS node_id
                FROM todo_dependency td
                WHERE td.prerequisite_id = :dependent_id
                  AND td.deleted_at IS NULL
                UNION ALL
                SELECT td.dependent_id
                FROM todo_dependency td
                JOIN downstream d ON td.prerequisite_id = d.node_id
                WHERE td.deleted_at IS NULL
            )
            SELECT node_id::text FROM downstream
            WHERE node_id = ANY(:prerequisite_ids::uuid[])
        """)

        result = await self.session.execute(
            sql,
            {
                "dependent_id": str(dependent_id),
                "prerequisite_ids": prereq_strs,
            },
        )
        return [UUID(row[0]) for row in result.fetchall()]

    async def get_subgraph_raw(self, todo_id: UUID) -> List[Tuple[str, str]]:
        """
        Return all (prerequisite_id, dependent_id) edges in the full
        upstream + downstream subgraph of `todo_id` using recursive CTEs.
        """
        sql = text("""
            WITH RECURSIVE upstream_edges AS (
                SELECT prerequisite_id, dependent_id
                FROM todo_dependency
                WHERE dependent_id = :todo_id AND deleted_at IS NULL
                UNION ALL
                SELECT td.prerequisite_id, td.dependent_id
                FROM todo_dependency td
                JOIN upstream_edges ue ON td.dependent_id = ue.prerequisite_id
                WHERE td.deleted_at IS NULL
            ),
            downstream_edges AS (
                SELECT prerequisite_id, dependent_id
                FROM todo_dependency
                WHERE prerequisite_id = :todo_id AND deleted_at IS NULL
                UNION ALL
                SELECT td.prerequisite_id, td.dependent_id
                FROM todo_dependency td
                JOIN downstream_edges de ON td.prerequisite_id = de.dependent_id
                WHERE td.deleted_at IS NULL
            ),
            all_edges AS (
                SELECT * FROM upstream_edges
                UNION
                SELECT * FROM downstream_edges
            )
            SELECT DISTINCT
                prerequisite_id::text,
                dependent_id::text
            FROM all_edges
        """)

        result = await self.session.execute(sql, {"todo_id": str(todo_id)})
        return [(row[0], row[1]) for row in result.fetchall()]

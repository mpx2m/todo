from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import TodoHistoryChangeBy, TodoStatus
from app.models.todo_history import TodoHistory


class HistoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        todo_id: UUID,
        from_status: TodoStatus,
        to_status: TodoStatus,
        changed_by: TodoHistoryChangeBy,
    ) -> TodoHistory:
        history = TodoHistory(
            todo_id=todo_id,
            from_status=from_status,
            to_status=to_status,
            changed_by=changed_by,
        )
        self.session.add(history)
        await self.session.flush()
        return history

    async def get_by_todo_id(self, todo_id: UUID) -> List[TodoHistory]:
        result = await self.session.execute(
            select(TodoHistory)
            .where(TodoHistory.todo_id == todo_id)
            .order_by(TodoHistory.created_at.desc())
        )
        return list(result.scalars().all())

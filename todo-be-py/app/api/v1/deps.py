from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repository.dependency_repo import DependencyRepository
from app.repository.history_repo import HistoryRepository
from app.repository.todo_repo import TodoRepository
from app.services.todo_service import TodoService


async def get_todo_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TodoService:
    return TodoService(
        todo_repo=TodoRepository(session),
        dep_repo=DependencyRepository(session),
        history_repo=HistoryRepository(session),
    )


ServiceDep = Annotated[TodoService, Depends(get_todo_service)]

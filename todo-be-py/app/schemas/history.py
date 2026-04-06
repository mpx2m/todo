from datetime import datetime
from uuid import UUID

from app.enums import TodoHistoryChangeBy, TodoStatus
from app.schemas.todo import CamelModel


class TodoHistoryResponse(CamelModel):
    id: UUID
    todo_id: UUID
    from_status: TodoStatus
    to_status: TodoStatus
    changed_by: TodoHistoryChangeBy
    created_at: datetime

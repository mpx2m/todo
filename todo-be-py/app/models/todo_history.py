from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Index
from sqlmodel import Field, SQLModel

from app.enums import TodoHistoryChangeBy, TodoStatus


class TodoHistory(SQLModel, table=True):
    __tablename__ = "todo_history"
    __table_args__ = (
        Index("idx_todo_history_todo_id_created_at", "todo_id", "created_at"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    todo_id: UUID = Field(foreign_key="todo.id")
    from_status: TodoStatus
    to_status: TodoStatus
    changed_by: TodoHistoryChangeBy
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False),
    )

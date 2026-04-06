from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Index, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from app.enums import TodoPriority, TodoStatus


class Todo(SQLModel, table=True):
    __tablename__ = "todo"
    __table_args__ = (
        Index("idx_todo_due_date", "due_date", postgresql_where=text("deleted_at IS NULL")),
        Index("idx_todo_status_due_date", "status", "due_date", postgresql_where=text("deleted_at IS NULL")),
        Index("idx_todo_priority_due_date", "priority", "due_date", postgresql_where=text("deleted_at IS NULL")),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    status: TodoStatus = Field(default=TodoStatus.NOT_STARTED)
    priority: TodoPriority = Field(default=TodoPriority.LOW)
    recurrence: Optional[dict] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False),
    )

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Index, text
from sqlmodel import Field, SQLModel


class TodoDependency(SQLModel, table=True):
    __tablename__ = "todo_dependency"
    __table_args__ = (
        # Partial unique index: (prerequisite_id, dependent_id) unique when not soft-deleted
        Index(
            "uq_todo_dependency_active",
            "prerequisite_id",
            "dependent_id",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
        Index("idx_todo_dependency_dependent", "dependent_id", postgresql_where=text("deleted_at IS NULL")),
        Index("idx_todo_dependency_prerequisite", "prerequisite_id", postgresql_where=text("deleted_at IS NULL")),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    prerequisite_id: UUID = Field(foreign_key="todo.id")
    dependent_id: UUID = Field(foreign_key="todo.id")
    deleted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False),
    )

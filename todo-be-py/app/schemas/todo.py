from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

from app.enums import DependencyStatus, Recurrence, RecurrenceUnit, TodoPriority, TodoStatus


class CamelModel(BaseModel):
    """Base model: accepts and outputs camelCase to stay compatible with existing frontend."""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class RecurrenceSchema(CamelModel):
    type: Recurrence
    interval: Optional[int] = None
    unit: Optional[RecurrenceUnit] = None


class TodoCreate(CamelModel):
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TodoStatus] = None
    priority: Optional[TodoPriority] = None
    recurrence: Optional[RecurrenceSchema] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be empty")
        return v


class TodoUpdate(CamelModel):
    name: Optional[str] = None
    # nullable fields: if explicitly set to None in the request → clear the field
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TodoStatus] = None
    priority: Optional[TodoPriority] = None
    recurrence: Optional[RecurrenceSchema] = None


class TodoResponse(CamelModel):
    id: UUID
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: TodoStatus
    priority: TodoPriority
    recurrence: Optional[RecurrenceSchema] = None
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    dependency_status: Optional[DependencyStatus] = None

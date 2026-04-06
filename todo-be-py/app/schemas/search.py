from typing import List, Optional
from uuid import UUID

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

from app.enums import DependencyStatus, SortBy, SortOrder, TodoPriority, TodoStatus
from app.schemas.todo import CamelModel, TodoResponse


class TodoSearchResponse(CamelModel):
    total: int
    page: int
    limit: int
    results: List[TodoResponse]

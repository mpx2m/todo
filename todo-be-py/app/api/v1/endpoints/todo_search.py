from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query

from app.api.v1.deps import ServiceDep
from app.enums import DependencyStatus, SortBy, SortOrder, TodoPriority, TodoStatus
from app.schemas.search import TodoSearchResponse

router = APIRouter()


@router.get("/search", response_model=TodoSearchResponse)
async def search_todos(
    service: ServiceDep,
    name: Optional[str] = None,
    status: Optional[TodoStatus] = None,
    priority: Optional[TodoPriority] = None,
    dueDateStart: Optional[datetime] = Query(None),
    dueDateEnd: Optional[datetime] = Query(None),
    dependencyStatus: Optional[DependencyStatus] = Query(None),
    sortBy: SortBy = Query(SortBy.DUE_DATE),
    sortOrder: SortOrder = Query(SortOrder.DESC),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
):
    return await service.search(
        name=name,
        status=status,
        priority=priority,
        due_date_start=dueDateStart,
        due_date_end=dueDateEnd,
        dependency_status=dependencyStatus,
        sort_by=sortBy,
        sort_order=sortOrder,
        page=page,
        limit=limit,
    )

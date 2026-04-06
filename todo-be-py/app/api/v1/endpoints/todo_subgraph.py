from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.api.v1.deps import ServiceDep
from app.schemas.history import TodoHistoryResponse
from app.schemas.subgraph import TodoSubgraph

router = APIRouter()


@router.get("/{id}/subgraph", response_model=TodoSubgraph)
async def get_subgraph(id: UUID, service: ServiceDep):
    return await service.get_subgraph(id)


@router.get("/{id}/history", response_model=List[TodoHistoryResponse])
async def get_history(id: UUID, service: ServiceDep):
    return await service.get_history(id)

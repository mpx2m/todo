from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.api.v1.deps import ServiceDep
from app.schemas.dependency import AddDependenciesRequest, DependencyMutationResult
from app.schemas.todo import TodoResponse

router = APIRouter()


@router.post("/{id}/dependencies", response_model=DependencyMutationResult)
async def add_dependencies(id: UUID, body: AddDependenciesRequest, service: ServiceDep):
    return await service.add_dependencies(id, body)


@router.delete("/{id}/dependencies", response_model=DependencyMutationResult)
async def remove_dependencies(id: UUID, body: AddDependenciesRequest, service: ServiceDep):
    return await service.remove_dependencies(id, body)


@router.get("/{id}/dependencies", response_model=List[TodoResponse])
async def list_dependencies(id: UUID, service: ServiceDep):
    return await service.list_dependencies(id)


@router.get("/{id}/dependents", response_model=List[TodoResponse])
async def list_dependents(id: UUID, service: ServiceDep):
    return await service.list_dependents(id)

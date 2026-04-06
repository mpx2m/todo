from uuid import UUID

from fastapi import APIRouter

from app.api.v1.deps import ServiceDep
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter()


@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(body: TodoCreate, service: ServiceDep):
    return await service.create(body)


@router.get("/{id}", response_model=TodoResponse)
async def get_todo(id: UUID, service: ServiceDep):
    return await service.find_one(id)


@router.patch("/{id}", response_model=TodoResponse)
async def update_todo(id: UUID, body: TodoUpdate, service: ServiceDep):
    return await service.update(id, body)


@router.delete("/{id}", response_model=TodoResponse)
async def delete_todo(id: UUID, service: ServiceDep):
    return await service.remove(id)

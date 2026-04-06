from fastapi import APIRouter

from app.api.v1.endpoints import todo_deps, todo_search, todo_subgraph, todos

router = APIRouter(prefix="/todo", tags=["todo"])

# Order matters: /search and /{id}/subgraph etc. must be registered
# before the generic /{id} catch-all routes.
router.include_router(todo_search.router)
router.include_router(todo_subgraph.router)
router.include_router(todo_deps.router)
router.include_router(todos.router)

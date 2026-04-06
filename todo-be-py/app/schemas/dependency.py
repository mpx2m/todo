from typing import List, Optional

from app.schemas.todo import CamelModel


class AddDependenciesRequest(CamelModel):
    prerequisite_ids: List[str] = []


class DependencyMutationResult(CamelModel):
    dependent_id: str
    created: Optional[int] = None
    removed: Optional[int] = None

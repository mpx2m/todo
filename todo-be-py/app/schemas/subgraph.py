from typing import List

from app.schemas.todo import CamelModel, TodoResponse


class SubgraphEdge(CamelModel):
    prerequisite_id: str
    dependent_id: str


class TodoSubgraph(CamelModel):
    root_id: str
    nodes: List[TodoResponse]
    edges: List[SubgraphEdge]

from typing import Literal
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.schemas import GraphResponse, TraversalResponse
from backend.app import crud

router = APIRouter(prefix="/graph", tags=["Graph"])

@router.get(
    "/",
    response_model=GraphResponse,
    summary="Get note-link graph",
    description="Returns the full knowledge network as nodes and edges for Cytoscape, D3, or other graph visualizers."
)
def get_graph(db: Session = Depends(get_db)):
    return crud.get_graph_data(db=db)

@router.get(
    "/traverse/{note_id}",
    response_model=TraversalResponse,
    summary="BFS / DFS Graph Traversal",
    description="Performs Breadth-First Search (BFS) or Depth-First Search (DFS) starting from a specific note, tracking visited depth, traversed edges, and cycle prevention."
)
def traverse_graph(
    note_id: int = Path(..., description="Root note ID to begin traversal from"),
    method: Literal["bfs", "dfs"] = Query("bfs", description="Traversal algorithm: 'bfs' or 'dfs'"),
    max_depth: int = Query(3, ge=1, le=10, description="Maximum traversal depth from starting note"),
    direction: Literal["outgoing", "incoming", "both"] = Query("outgoing", description="Link direction: 'outgoing', 'incoming', or 'both'"),
    db: Session = Depends(get_db)
):
    return crud.traverse_graph(
        db=db,
        note_id=note_id,
        method=method,
        max_depth=max_depth,
        direction=direction
    )

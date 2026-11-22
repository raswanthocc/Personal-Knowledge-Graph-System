from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class TagResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, description="Unique title of the note")
    content: Optional[str] = Field("", description="Markdown content with optional [[Wiki Links]]")
    tags: Optional[List[str]] = Field(default_factory=list, description="List of tags to associate")

class NoteCreate(NoteBase):
    selective_area: Optional[str] = Field(None, description="Optional domain scope for auto-linking")

class NoteListItem(BaseModel):
    id: int
    title: str
    content: Optional[str] = ""
    created_at: Optional[datetime] = None
    tags: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class NoteSummary(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)

class NoteDetailResponse(BaseModel):
    id: int
    title: str
    content: Optional[str] = ""
    created_at: Optional[datetime] = None
    tags: List[str] = []
    linked_notes: List[NoteSummary] = Field(default_factory=list, description="Outgoing notes linked from this note")
    backlinks: List[NoteSummary] = Field(default_factory=list, description="Incoming notes linking to this note")

    model_config = ConfigDict(from_attributes=True)

class LinkCreate(BaseModel):
    target_id: int = Field(..., description="Target note ID to establish link towards")

class LinkResponse(BaseModel):
    source_id: int
    target_id: int
    message: str = "Link established successfully"

class GraphNode(BaseModel):
    id: int
    title: str
    tags: List[str] = []

class GraphEdge(BaseModel):
    source: int
    target: int

class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

class TraversalNode(BaseModel):
    id: int
    title: str
    depth: int
    tags: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class TraversalEdge(BaseModel):
    source: int
    target: int
    depth: int

class TraversalResponse(BaseModel):
    start_note_id: int
    start_note_title: str
    method: str
    direction: str
    max_depth: int
    total_nodes_visited: int
    visited_nodes: List[TraversalNode]
    edges: List[TraversalEdge]
    traversal_order: List[int]

class TagSuggestionResponse(BaseModel):
    tags: List[str]

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.schemas import (
    NoteCreate,
    NoteListItem,
    NoteDetailResponse,
    LinkCreate,
    LinkResponse
)
from backend.app import crud

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post(
    "/",
    response_model=NoteDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Creates a note with title, markdown content, and tags. Resolves [[Wiki Links]] and tags automatically."
)
def create_note(
    note_in: NoteCreate,
    db: Session = Depends(get_db)
):
    return crud.create_note(db=db, note_in=note_in)

@router.get(
    "/",
    response_model=List[NoteListItem],
    summary="Get all notes",
    description="Retrieve all notes, with optional filtering by tag or keyword search in title/content."
)
def get_notes(
    tag: Optional[str] = Query(None, description="Filter by tag name (e.g. 'productivity')"),
    keyword: Optional[str] = Query(None, description="Search keyword in title or content"),
    db: Session = Depends(get_db)
):
    return crud.get_all_notes(db=db, tag=tag, keyword=keyword)

@router.get(
    "/{note_id}",
    response_model=NoteDetailResponse,
    summary="Get note details",
    description="Retrieve detailed information about a note, including outgoing linked notes and incoming backlinks."
)
def get_note_by_id(
    note_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_note_detail(db=db, note_id=note_id)

@router.patch(
    "/{note_id}/link",
    response_model=LinkResponse,
    summary="Create a link from one note to another",
    description="Creates a directed link from note_id (source) to target_id (target). Rejects self-loops and duplicates."
)
def link_note(
    note_id: int,
    link_in: LinkCreate,
    db: Session = Depends(get_db)
):
    res = crud.create_manual_link(db=db, source_id=note_id, target_id=link_in.target_id)
    return LinkResponse(**res)

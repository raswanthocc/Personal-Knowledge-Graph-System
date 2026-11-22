from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.schemas import TagSuggestionResponse
from backend.app.logic.tag_manager import get_tag_suggestions

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get(
    "/suggestions/",
    response_model=TagSuggestionResponse,
    summary="Get tag suggestions",
    description="Provides autocomplete suggestions from existing normalized tags."
)
def tag_suggestions(
    query: Optional[str] = Query(None, description="Prefix or search query for tag"),
    db: Session = Depends(get_db)
):
    tags = get_tag_suggestions(db, query=query)
    return TagSuggestionResponse(tags=tags)

@router.get(
    "/areas/",
    response_model=TagSuggestionResponse,
    summary="Get core domain areas",
    description="Returns list of main topical areas for selective coverage dropdown."
)
def get_domain_areas(db: Session = Depends(get_db)):
    # Standard 6 core domains plus any active user tags
    base_areas = ["python", "ml", "nlp", "database", "frontend", "graphs"]
    existing = get_tag_suggestions(db, limit=50)
    all_areas = list(dict.fromkeys(base_areas + existing))
    return TagSuggestionResponse(tags=all_areas)

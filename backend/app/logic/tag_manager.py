import re
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.models import Tag

def normalize_tag(tag_str: str) -> str:
    """
    Normalizes tag:
    - Strips leading '#' or '@'
    - Trims whitespace
    - Converts to lowercase
    - Replaces internal spaces with hyphens
    """
    if not tag_str:
        return ""
    cleaned = tag_str.strip().lstrip("#@").strip().lower()
    cleaned = re.sub(r"\s+", "-", cleaned)
    # Remove any unwanted special characters keeping letters, digits, and hyphens
    cleaned = re.sub(r"[^a-z0-9\-]", "", cleaned)
    return cleaned

def get_or_create_tag(db: Session, tag_name: str) -> Optional[Tag]:
    normalized = normalize_tag(tag_name)
    if not normalized:
        return None
    tag = db.query(Tag).filter(Tag.name == normalized).first()
    if not tag:
        tag = Tag(name=normalized)
        db.add(tag)
        db.flush()
    return tag

def get_tag_suggestions(db: Session, query: Optional[str] = None, limit: int = 20) -> List[str]:
    q = db.query(Tag.name)
    if query:
        norm_query = normalize_tag(query)
        if norm_query:
            q = q.filter(Tag.name.like(f"%{norm_query}%"))
    tags = q.order_by(Tag.name).limit(limit).all()
    return [t[0] for t in tags]

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from fastapi import HTTPException, status
from backend.app.models import Note, Link, Tag, NoteTag
from collections import deque
from backend.app.schemas import (
    NoteCreate, NoteListItem, NoteDetailResponse, NoteSummary,
    GraphResponse, GraphNode, GraphEdge,
    TraversalResponse, TraversalNode, TraversalEdge
)
from backend.app.logic.tag_manager import normalize_tag, get_or_create_tag
from backend.app.logic.wiki_parser import extract_wiki_links, extract_inline_tags
from backend.app.logic.auto_linker import find_auto_link_candidates

def get_note_by_id(db: Session, note_id: int) -> Optional[Note]:
    return db.query(Note).filter(Note.id == note_id).first()

def get_note_by_title(db: Session, title: str) -> Optional[Note]:
    norm_title = title.strip().lower()
    return db.query(Note).filter(func.lower(func.trim(Note.title)) == norm_title).first()

def get_all_notes(
    db: Session,
    tag: Optional[str] = None,
    keyword: Optional[str] = None
) -> List[NoteListItem]:
    query = db.query(Note)

    if tag:
        normalized_tag = normalize_tag(tag)
        if normalized_tag:
            query = query.join(Note.note_tags).join(NoteTag.tag).filter(Tag.name == normalized_tag)

    if keyword:
        kw = f"%{keyword.strip().lower()}%"
        query = query.filter(
            or_(
                func.lower(Note.title).like(kw),
                func.lower(Note.content).like(kw)
            )
        )

    notes = query.order_by(Note.created_at.desc()).all()
    result = []
    for note in notes:
        tag_names = [nt.tag.name for nt in note.note_tags if nt.tag]
        result.append(
            NoteListItem(
                id=note.id,
                title=note.title,
                content=note.content or "",
                created_at=note.created_at,
                tags=tag_names
            )
        )
    return result

def get_note_detail(db: Session, note_id: int) -> NoteDetailResponse:
    note = get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found"
        )

    tags = [nt.tag.name for nt in note.note_tags if nt.tag]

    # Outgoing links: notes that this note links to
    outgoing = (
        db.query(Note)
        .join(Link, Link.target_id == Note.id)
        .filter(Link.source_id == note_id)
        .all()
    )
    linked_notes = [NoteSummary(id=n.id, title=n.title) for n in outgoing]

    # Backlinks: notes that link to this note
    incoming = (
        db.query(Note)
        .join(Link, Link.source_id == Note.id)
        .filter(Link.target_id == note_id)
        .all()
    )
    backlinks = [NoteSummary(id=n.id, title=n.title) for n in incoming]

    return NoteDetailResponse(
        id=note.id,
        title=note.title,
        content=note.content or "",
        created_at=note.created_at,
        tags=tags,
        linked_notes=linked_notes,
        backlinks=backlinks
    )

def create_link_internal(db: Session, source_id: int, target_id: int) -> bool:
    """Safely adds a link between source and target, avoiding self-links and duplicates."""
    if source_id == target_id:
        return False
    # Check pending objects in session
    for obj in db.new:
        if isinstance(obj, Link) and obj.source_id == source_id and obj.target_id == target_id:
            return False
    existing = db.query(Link).filter(
        Link.source_id == source_id,
        Link.target_id == target_id
    ).first()
    if not existing:
        link = Link(source_id=source_id, target_id=target_id)
        db.add(link)
        db.flush()
        return True
    return False

def create_note(db: Session, note_in: NoteCreate) -> NoteDetailResponse:
    clean_title = note_in.title.strip()
    if not clean_title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty")

    # Check unique title constraint
    existing = get_note_by_title(db, clean_title)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A note with title '{clean_title}' already exists"
        )

    # 1. Create Note record
    new_note = Note(title=clean_title, content=note_in.content or "")
    db.add(new_note)
    db.flush()

    # 2. Attach normalized tags (combining explicit tags and inline tags [#tag], [[#tag]], #tag)
    all_raw_tags = list(note_in.tags or [])
    inline_tags = extract_inline_tags(f"{clean_title} {note_in.content or ''}")
    for it in inline_tags:
        if it not in all_raw_tags:
            all_raw_tags.append(it)

    normalized_tag_names = []
    for t in all_raw_tags:
        tag_obj = get_or_create_tag(db, t)
        if tag_obj and tag_obj.name not in normalized_tag_names:
            db.add(NoteTag(note_id=new_note.id, tag_id=tag_obj.id))
            normalized_tag_names.append(tag_obj.name)
    db.flush()

    # 3. Hidden Logic Rule 1: Auto-resolve [[Wiki Links]] in content
    wiki_titles = extract_wiki_links(note_in.content or "")
    for w_title in wiki_titles:
        target_note = get_note_by_title(db, w_title)
        if target_note and target_note.id != new_note.id:
            create_link_internal(db, source_id=new_note.id, target_id=target_note.id)
        else:
            # If bracket matches an existing tag name (e.g. [[python]]), link to top note with that tag
            norm_w = normalize_tag(w_title)
            tag_match = db.query(Tag).filter(Tag.name == norm_w).first()
            if tag_match:
                tagged_note = (
                    db.query(Note)
                    .join(Note.note_tags)
                    .filter(NoteTag.tag_id == tag_match.id, Note.id != new_note.id)
                    .first()
                )
                if tagged_note:
                    create_link_internal(db, source_id=new_note.id, target_id=tagged_note.id)

    # 4. Forward reference resolution: check if any prior note referenced [[new_note.title]]
    all_notes = db.query(Note).filter(Note.id != new_note.id).all()
    for prior_note in all_notes:
        if prior_note.content:
            prior_wikis = extract_wiki_links(prior_note.content)
            for pw in prior_wikis:
                if pw.strip().lower() == clean_title.lower():
                    create_link_internal(db, source_id=prior_note.id, target_id=new_note.id)

    # 5. Finalized Automatic Linking (Tag overlap / Semantic Fallback)
    auto_candidate_ids = find_auto_link_candidates(
        db=db,
        current_note_id=new_note.id,
        tags=normalized_tag_names,
        title=clean_title,
        content=note_in.content or "",
        selective_area=note_in.selective_area,
        top_k=3
    )
    for cid in auto_candidate_ids:
        create_link_internal(db, source_id=new_note.id, target_id=cid)

    db.commit()
    db.refresh(new_note)

    return get_note_detail(db, new_note.id)

def create_manual_link(db: Session, source_id: int, target_id: int) -> dict:
    if source_id == target_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Self-loops are not allowed: A note cannot link to itself"
        )

    source = get_note_by_id(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source note with ID {source_id} not found"
        )

    target = get_note_by_id(db, target_id)
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target note with ID {target_id} not found"
        )

    existing = db.query(Link).filter(
        Link.source_id == source_id,
        Link.target_id == target_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Link from Note {source_id} to Note {target_id} already exists"
        )

    link = Link(source_id=source_id, target_id=target_id)
    db.add(link)
    db.commit()

    return {
        "source_id": source_id,
        "target_id": target_id,
        "message": f"Successfully created link from '{source.title}' to '{target.title}'"
    }

def get_graph_data(db: Session) -> GraphResponse:
    notes = db.query(Note).all()
    links = db.query(Link).all()

    nodes = []
    for note in notes:
        tag_names = [nt.tag.name for nt in note.note_tags if nt.tag]
        nodes.append(GraphNode(id=note.id, title=note.title, tags=tag_names))

    edges = [GraphEdge(source=link.source_id, target=link.target_id) for link in links]
    return GraphResponse(nodes=nodes, edges=edges)

def traverse_graph(
    db: Session,
    note_id: int,
    method: str = "bfs",
    max_depth: int = 3,
    direction: str = "outgoing"
) -> TraversalResponse:
    start_note = get_note_by_id(db, note_id)
    if not start_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found"
        )

    method = method.lower().strip()
    if method not in ("bfs", "dfs"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid traversal method '{method}'. Allowed methods: 'bfs', 'dfs'."
        )

    direction = direction.lower().strip()
    if direction not in ("outgoing", "incoming", "both"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid traversal direction '{direction}'. Allowed: 'outgoing', 'incoming', 'both'."
        )

    # Pre-fetch all notes lookup for titles and tags
    all_notes = {n.id: n for n in db.query(Note).all()}

    def get_tags(n: Note) -> List[str]:
        return [nt.tag.name for nt in n.note_tags if nt.tag]

    def get_adj_edges(curr_id: int):
        res = []
        if direction in ("outgoing", "both"):
            out_links = db.query(Link).filter(Link.source_id == curr_id).all()
            for l in out_links:
                res.append((l.target_id, l.source_id, l.target_id))
        if direction in ("incoming", "both"):
            in_links = db.query(Link).filter(Link.target_id == curr_id).all()
            for l in in_links:
                res.append((l.source_id, l.source_id, l.target_id))
        return res

    visited_nodes: List[TraversalNode] = []
    edges_traversed: List[TraversalEdge] = []
    traversal_order: List[int] = []
    visited = set()

    if method == "bfs":
        queue = deque([(note_id, 0)])
        visited.add(note_id)
        traversal_order.append(note_id)
        visited_nodes.append(TraversalNode(
            id=start_note.id,
            title=start_note.title,
            depth=0,
            tags=get_tags(start_note)
        ))

        while queue:
            curr_id, depth = queue.popleft()
            if depth >= max_depth:
                continue

            for neighbor_id, src, tgt in get_adj_edges(curr_id):
                if neighbor_id not in visited and neighbor_id in all_notes:
                    visited.add(neighbor_id)
                    neighbor_note = all_notes[neighbor_id]
                    queue.append((neighbor_id, depth + 1))
                    traversal_order.append(neighbor_id)
                    visited_nodes.append(TraversalNode(
                        id=neighbor_note.id,
                        title=neighbor_note.title,
                        depth=depth + 1,
                        tags=get_tags(neighbor_note)
                    ))
                    edges_traversed.append(TraversalEdge(source=src, target=tgt, depth=depth + 1))
                elif neighbor_id in visited and depth + 1 <= max_depth:
                    edge_exists = any(e.source == src and e.target == tgt for e in edges_traversed)
                    if not edge_exists:
                        edges_traversed.append(TraversalEdge(source=src, target=tgt, depth=depth + 1))

    else:  # DFS
        def dfs(curr_id: int, depth: int):
            visited.add(curr_id)
            traversal_order.append(curr_id)
            curr_note = all_notes[curr_id]
            visited_nodes.append(TraversalNode(
                id=curr_note.id,
                title=curr_note.title,
                depth=depth,
                tags=get_tags(curr_note)
            ))

            if depth >= max_depth:
                return

            for neighbor_id, src, tgt in get_adj_edges(curr_id):
                if neighbor_id not in visited and neighbor_id in all_notes:
                    edges_traversed.append(TraversalEdge(source=src, target=tgt, depth=depth + 1))
                    dfs(neighbor_id, depth + 1)
                elif neighbor_id in visited and depth + 1 <= max_depth:
                    edge_exists = any(e.source == src and e.target == tgt for e in edges_traversed)
                    if not edge_exists:
                        edges_traversed.append(TraversalEdge(source=src, target=tgt, depth=depth + 1))

        dfs(note_id, 0)

    return TraversalResponse(
        start_note_id=start_note.id,
        start_note_title=start_note.title,
        method=method,
        direction=direction,
        max_depth=max_depth,
        total_nodes_visited=len(visited_nodes),
        visited_nodes=visited_nodes,
        edges=edges_traversed,
        traversal_order=traversal_order
    )

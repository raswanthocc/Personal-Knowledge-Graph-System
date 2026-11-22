import re
from typing import List, Set, Optional
from sqlalchemy.orm import Session
from backend.app.models import Note, Tag, NoteTag

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further",
    "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me", "more", "most", "my",
    "myself", "no", "nor", "not", "now", "of", "off", "on", "once", "only", "or", "other", "our",
    "ours", "ourselves", "out", "over", "own", "same", "she", "should", "so", "some", "such", "than",
    "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "were", "what",
    "when", "where", "which", "while", "who", "whom", "why", "with", "would", "you", "your", "yours",
    "using", "based", "models", "guide", "intro", "introduction"
}

def stem_token(word: str) -> str:
    """Lightweight suffix stemmer for matching morphological variations."""
    w = word.lower()
    for suffix in ("ing", "tions", "tion", "ies", "es", "ed", "ment", "ments", "ers", "er", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 3:
            return w[:-len(suffix)]
    return w

def tokenize_and_stem(text: str) -> Set[str]:
    """
    Tokenizes text, strips stopwords, and produces base stems.
    Decomposes compound terms like 'quantum-machine-learning' -> {'quantum', 'machine', 'learn'}.
    """
    if not text:
        return set()
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    tokens = re.findall(r"\b[a-zA-Z0-9]{3,}\b", cleaned.lower())
    results = set()
    for t in tokens:
        if t not in STOPWORDS:
            results.add(t)
            stem = stem_token(t)
            if stem not in STOPWORDS:
                results.add(stem)
    return results

def find_auto_link_candidates(
    db: Session,
    current_note_id: int,
    tags: List[str],
    title: str,
    content: str,
    selective_area: str = None,
    top_k: int = 3
) -> List[int]:
    """
    Token and Ranking Auto-Linker:
    1. Direct Tag Overlap: +4.0 per exact normalized tag match.
    2. Token & Stemming Concept Ranking:
       - Match in Title: +3.0
       - Match in Existing Tags: +2.5
       - Match in Content: +1.0
    3. Selective Area Scope: restricts candidates to domain area if chosen.
    4. Top-K Cutoff: connects to at most top_k highest scoring notes (score >= 1.5).
    """
    candidate_scores = {}  # note_id -> score

    # Query notes in selective area if requested
    allowed_note_ids: Optional[Set[int]] = None
    if selective_area:
        area_tag = selective_area.strip().lower()
        subq = (
            db.query(NoteTag.note_id)
            .join(Tag, Tag.id == NoteTag.tag_id)
            .filter(Tag.name == area_tag)
            .all()
        )
        found_ids = {row[0] for row in subq}
        if found_ids:
            allowed_note_ids = found_ids

    # 1. Exact Tag Match scoring
    if tags:
        for tag_name in tags:
            tag_obj = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag_obj:
                continue
            matching_notes = (
                db.query(NoteTag.note_id)
                .filter(NoteTag.tag_id == tag_obj.id, NoteTag.note_id != current_note_id)
                .all()
            )
            for (nid,) in matching_notes:
                if allowed_note_ids is not None and nid not in allowed_note_ids:
                    continue
                candidate_scores[nid] = candidate_scores.get(nid, 0.0) + 4.0

    # 2. Token & Stemming Concept Ranking
    source_tokens = tokenize_and_stem(f"{title} {content} {' '.join(tags or [])}")

    if source_tokens:
        existing_notes = (
            db.query(Note.id, Note.title, Note.content)
            .filter(Note.id != current_note_id)
            .all()
        )

        # Batch load existing note tags
        note_tags_map = {}
        for nid, tag_name in (
            db.query(NoteTag.note_id, Tag.name)
            .join(Tag, Tag.id == NoteTag.tag_id)
            .filter(NoteTag.note_id != current_note_id)
            .all()
        ):
            note_tags_map.setdefault(nid, []).append(tag_name)

        for (nid, ntitle, ncontent) in existing_notes:
            if allowed_note_ids is not None and nid not in allowed_note_ids:
                continue

            title_tokens = tokenize_and_stem(ntitle)
            tag_tokens = tokenize_and_stem(" ".join(note_tags_map.get(nid, [])))
            content_tokens = tokenize_and_stem(ncontent or "")

            title_hits = len(source_tokens.intersection(title_tokens))
            tag_hits = len(source_tokens.intersection(tag_tokens))
            content_hits = len(source_tokens.intersection(content_tokens))

            concept_score = (title_hits * 3.0) + (tag_hits * 2.5) + (content_hits * 1.0)
            if concept_score > 0:
                candidate_scores[nid] = candidate_scores.get(nid, 0.0) + concept_score

    # Sort descending by score and apply Top-K cutoff
    sorted_candidates = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
    selected_ids = [nid for nid, score in sorted_candidates[:top_k] if score >= 1.5]
    return selected_ids

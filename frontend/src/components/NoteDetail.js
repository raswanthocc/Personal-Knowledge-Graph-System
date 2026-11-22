import React from "react";

function NoteDetail({ note, onSelectWikiLink, onOpenLinkModal }) {
  if (!note) {
    return (
      <div className="detail-panel" style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: "#64748b", textAlign: "center" }}>
          Select a note to inspect its content, outgoing links, and backlinks.
        </div>
      </div>
    );
  }

  // Parse markdown content and replace [[Title]] with clickable wiki links
  const renderContentWithWikiLinks = (text) => {
    if (!text) return "No content provided.";
    const parts = [];
    const regex = /\[\[(.*?)\]\]/g;
    let lastIndex = 0;
    let match;

    while ((match = regex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        parts.push(text.substring(lastIndex, match.index));
      }
      const wikiTitle = match[1];
      parts.push(
        <button
          key={match.index}
          className="wiki-link-btn"
          onClick={() => onSelectWikiLink(wikiTitle)}
        >
          [[{wikiTitle}]]
        </button>
      );
      lastIndex = regex.lastIndex;
    }

    if (lastIndex < text.length) {
      parts.push(text.substring(lastIndex));
    }
    return parts;
  };

  return (
    <div className="detail-panel">
      <div className="detail-header">
        <div>
          <h2 className="detail-title">{note.title}</h2>
          <div style={{ display: "flex", gap: "6px", flexWrap: "wrap", marginTop: "6px" }}>
            {note.tags.map((t) => (
              <span key={t} className="tag-pill" style={{ borderColor: "#06b6d4", color: "#38bdf8" }}>
                #{t}
              </span>
            ))}
          </div>
        </div>
        <button className="btn btn-secondary" onClick={() => onOpenLinkModal(note.id)}>
          + Link Note
        </button>
      </div>

      <div className="section-label">Note Content</div>
      <div className="detail-content">{renderContentWithWikiLinks(note.content)}</div>

      <div className="section-label">Outgoing Links ({note.linked_notes?.length || 0})</div>
      <div className="links-list">
        {note.linked_notes && note.linked_notes.length > 0 ? (
          note.linked_notes.map((l) => (
            <div key={l.id} className="link-item" onClick={() => onSelectWikiLink(l.title)}>
              <span>→ {l.title}</span>
              <span style={{ fontSize: "11px", color: "#94a3b8" }}>ID: {l.id}</span>
            </div>
          ))
        ) : (
          <div style={{ color: "#64748b", fontSize: "13px" }}>No outgoing links.</div>
        )}
      </div>

      <div className="section-label">Backlinks / Incoming ({note.backlinks?.length || 0})</div>
      <div className="links-list">
        {note.backlinks && note.backlinks.length > 0 ? (
          note.backlinks.map((b) => (
            <div key={b.id} className="link-item" onClick={() => onSelectWikiLink(b.title)}>
              <span>← {b.title}</span>
              <span style={{ fontSize: "11px", color: "#94a3b8" }}>ID: {b.id}</span>
            </div>
          ))
        ) : (
          <div style={{ color: "#64748b", fontSize: "13px" }}>No incoming backlinks.</div>
        )}
      </div>
    </div>
  );
}

export default NoteDetail;

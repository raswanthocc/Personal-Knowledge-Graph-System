import React from "react";

function NoteList({ notes, activeNoteId, onSelectNote, searchQuery, onSearchChange, tags, activeTag, onTagSelect }) {
  return (
    <div className="sidebar-panel">
      <div className="sidebar-header">
        <input
          type="text"
          className="search-input"
          placeholder="Search by keyword or title..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
        />
        <div className="tag-filter-list">
          <span
            className={`tag-pill ${!activeTag ? "active" : ""}`}
            onClick={() => onTagSelect("")}
          >
            All
          </span>
          {tags.map((tag) => (
            <span
              key={tag}
              className={`tag-pill ${activeTag === tag ? "active" : ""}`}
              onClick={() => onTagSelect(activeTag === tag ? "" : tag)}
            >
              #{tag}
            </span>
          ))}
        </div>
      </div>

      <div className="notes-list">
        {notes.length === 0 ? (
          <div style={{ textAlign: "center", color: "#64748b", padding: "20px" }}>
            No notes found.
          </div>
        ) : (
          notes.map((note) => (
            <div
              key={note.id}
              className={`note-card ${activeNoteId === note.id ? "active" : ""}`}
              onClick={() => onSelectNote(note.id)}
            >
              <div className="note-card-title">{note.title}</div>
              <div className="note-card-preview">
                {note.content ? note.content.slice(0, 70) : "No content"}
              </div>
              <div className="note-card-tags">
                {note.tags.map((t) => (
                  <span key={t} className="tag-pill">
                    #{t}
                  </span>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default NoteList;

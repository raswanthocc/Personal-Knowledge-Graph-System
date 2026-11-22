import React, { useState, useEffect } from "react";
import { getDomainAreas, getTagSuggestions } from "../api/axiosClient";

function NoteEditor({ isOpen, onClose, onSave }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tagInput, setTagInput] = useState("");
  const [selectiveArea, setSelectiveArea] = useState("");
  const [areaOptions, setAreaOptions] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isOpen) {
      getDomainAreas().then(setAreaOptions).catch(() => {});
      setTitle("");
      setContent("");
      setTagInput("");
      setSelectiveArea("");
      setError("");
    }
  }, [isOpen]);

  const handleTagChange = async (e) => {
    const val = e.target.value;
    setTagInput(val);
    const lastWord = val.split(",").pop().trim();
    if (lastWord.length >= 1) {
      try {
        const fetched = await getTagSuggestions(lastWord);
        setSuggestions(fetched);
      } catch (err) {
        setSuggestions([]);
      }
    } else {
      setSuggestions([]);
    }
  };

  const applySuggestion = (sug) => {
    const parts = tagInput.split(",").map((p) => p.trim());
    parts.pop();
    parts.push(sug);
    setTagInput(parts.join(", ") + ", ");
    setSuggestions([]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setError("Note title is required");
      return;
    }
    const tagsArray = tagInput
      .split(",")
      .map((t) => t.trim())
      .filter((t) => t.length > 0);

    onSave({
      title: title.trim(),
      content,
      tags: tagsArray,
      selective_area: selectiveArea || null,
    });
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2 style={{ marginBottom: "16px", color: "#fff" }}>Create New Note</h2>
        {error && <div style={{ color: "#f43f5e", marginBottom: "12px", fontSize: "13px" }}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Title (Unique)</label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g. Transformers & Self-Attention"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Selective Area Coverage (Domain Filter)</label>
            <select
              className="form-select"
              value={selectiveArea}
              onChange={(e) => setSelectiveArea(e.target.value)}
            >
              <option value="">-- General (No Specific Scope) --</option>
              {areaOptions.map((area) => (
                <option key={area} value={area}>
                  {area.toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Tags (comma-separated)</label>
            <input
              type="text"
              className="form-input"
              placeholder="ai, deep-learning, nlp"
              value={tagInput}
              onChange={handleTagChange}
            />
            {suggestions.length > 0 && (
              <div style={{ marginTop: "6px", display: "flex", gap: "6px", flexWrap: "wrap" }}>
                <span style={{ fontSize: "11px", color: "#94a3b8" }}>Suggestions:</span>
                {suggestions.map((s) => (
                  <span
                    key={s}
                    className="tag-pill"
                    style={{ background: "#334155", color: "#38bdf8" }}
                    onClick={() => applySuggestion(s)}
                  >
                    #{s}
                  </span>
                ))}
              </div>
            )}
          </div>

          <div className="form-group">
            <label className="form-label">Content (Supports markdown and [[Wiki Links]])</label>
            <textarea
              className="form-textarea"
              placeholder="Write your note here. Reference other notes using [[Note Title]] syntax..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              Save & Auto-Connect
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default NoteEditor;

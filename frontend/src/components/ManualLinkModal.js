import React, { useState } from "react";

function ManualLinkModal({ isOpen, onClose, currentNoteId, allNotes, onConfirmLink }) {
  const [targetId, setTargetId] = useState("");
  const [error, setError] = useState("");

  if (!isOpen) return null;

  const currentNote = allNotes.find((n) => n.id === currentNoteId);
  const eligibleNotes = allNotes.filter((n) => n.id !== currentNoteId);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!targetId) {
      setError("Please select a target note");
      return;
    }
    if (parseInt(targetId) === currentNoteId) {
      setError("Self-loops are not allowed: Cannot link a note to itself");
      return;
    }
    onConfirmLink(currentNoteId, parseInt(targetId));
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3 style={{ color: "#fff", marginBottom: "12px" }}>
          Link from "{currentNote?.title}"
        </h3>
        {error && <div style={{ color: "#f43f5e", marginBottom: "12px", fontSize: "13px" }}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Select Target Note</label>
            <select
              className="form-select"
              value={targetId}
              onChange={(e) => {
                setTargetId(e.target.value);
                setError("");
              }}
            >
              <option value="">-- Choose Note --</option>
              {eligibleNotes.map((note) => (
                <option key={note.id} value={note.id}>
                  {note.title} (ID: {note.id})
                </option>
              ))}
            </select>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              Create Link
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ManualLinkModal;

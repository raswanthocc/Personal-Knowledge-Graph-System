import React, { useState, useEffect, useCallback } from "react";
import {
  getNotes,
  getNoteDetail,
  createNote,
  linkNotes,
  getGraphData,
  getTagSuggestions,
} from "./api/axiosClient";
import NoteList from "./components/NoteList";
import NoteDetail from "./components/NoteDetail";
import NoteEditor from "./components/NoteEditor";
import ManualLinkModal from "./components/ManualLinkModal";
import GraphContainer from "./components/visualizations/GraphContainer";

function App() {
  const [allNotes, setAllNotes] = useState([]);
  const [filteredNotes, setFilteredNotes] = useState([]);
  const [activeNote, setActiveNote] = useState(null);
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [tags, setTags] = useState([]);
  const [activeTag, setActiveTag] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [isLinkModalOpen, setIsLinkModalOpen] = useState(false);
  const [linkingSourceId, setLinkingSourceId] = useState(null);

  const fetchNotesAndGraph = useCallback(async () => {
    try {
      const isFiltered = Boolean(activeTag || searchQuery);
      const [fetchedAllNotes, fetchedFilteredNotes, fetchedGraph, fetchedTags] =
        await Promise.all([
          getNotes(), // Always retrieve all notes in the knowledge graph
          isFiltered
            ? getNotes({
                tag: activeTag || undefined,
                keyword: searchQuery || undefined,
              })
            : null,
          getGraphData(),
          getTagSuggestions(),
        ]);

      setAllNotes(fetchedAllNotes);
      const currentFiltered = isFiltered ? fetchedFilteredNotes : fetchedAllNotes;
      setFilteredNotes(currentFiltered);
      setGraphData(fetchedGraph);
      setTags(fetchedTags);

      if (currentFiltered.length > 0 && !activeNote) {
        // Load first note details
        const detail = await getNoteDetail(currentFiltered[0].id);
        setActiveNote(detail);
      }
    } catch (err) {
      console.error("Failed to load initial data", err);
    }
  }, [activeTag, searchQuery, activeNote]);

  useEffect(() => {
    fetchNotesAndGraph();
  }, [fetchNotesAndGraph]);

  const handleSelectNote = async (noteId) => {
    try {
      const detail = await getNoteDetail(noteId);
      setActiveNote(detail);

      // If the selected note is currently hidden by active filter, reset filter so it shows in the sidebar list
      if (activeTag || searchQuery) {
        const isVisibleInList = filteredNotes.some((n) => n.id === noteId);
        if (!isVisibleInList) {
          setActiveTag("");
          setSearchQuery("");
        }
      }
    } catch (err) {
      console.error("Failed to fetch note detail", err);
    }
  };

  const handleSelectWikiLink = async (title) => {
    const cleanTitle = title.trim().toLowerCase();
    // 1. Search in allNotes first (independent of current filter)
    let matched = allNotes.find(
      (n) => n.title.toLowerCase() === cleanTitle
    );

    // 2. Fallback: Search backend directly if not in memory
    if (!matched) {
      try {
        const searchResults = await getNotes({ keyword: title.trim() });
        matched = searchResults.find(
          (n) => n.title.toLowerCase() === cleanTitle
        ) || searchResults[0];
      } catch (e) {
        console.error("Error searching note by title", e);
      }
    }

    if (matched) {
      // If the matched note is currently filtered out, reset activeTag and searchQuery
      const isVisibleInList = filteredNotes.some((n) => n.id === matched.id);
      if (!isVisibleInList) {
        setActiveTag("");
        setSearchQuery("");
      }
      handleSelectNote(matched.id);
    } else {
      alert(`Note titled "${title}" was not found. You can create it!`);
    }
  };

  const handleSaveNote = async (newNoteData) => {
    try {
      const created = await createNote(newNoteData);
      setIsEditorOpen(false);
      await fetchNotesAndGraph();
      setActiveNote(created);
    } catch (err) {
      alert(
        err.response?.data?.detail || "Failed to create note. Please check inputs."
      );
    }
  };

  const handleConfirmLink = async (sourceId, targetId) => {
    try {
      await linkNotes(sourceId, targetId);
      setIsLinkModalOpen(false);
      // Refresh note detail, all notes and graph
      const [updatedDetail, updatedGraph, updatedAllNotes] = await Promise.all([
        getNoteDetail(sourceId),
        getGraphData(),
        getNotes(),
      ]);
      setActiveNote(updatedDetail);
      setGraphData(updatedGraph);
      setAllNotes(updatedAllNotes);
    } catch (err) {
      alert(
        err.response?.data?.detail || "Failed to link notes. Verify relationship."
      );
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-left">
          <div className="logo-badge">PKGraph</div>
          <div>
            <div className="header-title">Personal Knowledge Graph</div>
            <div className="header-subtitle">
              Bi-directional Markdown Linking & Semantic Graph Traversal
            </div>
          </div>
        </div>
        <div className="header-actions">
          <button
            className="btn btn-secondary"
            onClick={fetchNotesAndGraph}
            title="Refresh knowledge graph"
          >
            🔄 Refresh
          </button>
          <button
            className="btn btn-primary"
            onClick={() => setIsEditorOpen(true)}
          >
            + New Note
          </button>
        </div>
      </header>

      <div className="main-layout">
        {/* Left: Filtered Notes List & Search */}
        <NoteList
          notes={filteredNotes}
          activeNoteId={activeNote?.id}
          onSelectNote={handleSelectNote}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          tags={tags}
          activeTag={activeTag}
          onTagSelect={setActiveTag}
        />

        {/* Center: Interactive Visualizations (Force Graph, Word Constellation, Radial Tree) */}
        <GraphContainer
          graphData={graphData}
          onSelectNode={handleSelectNote}
          activeNodeId={activeNote?.id}
        />

        {/* Right: Note Detail, Markdown Content, Outgoing Links & Backlinks */}
        <NoteDetail
          note={activeNote}
          onSelectWikiLink={handleSelectWikiLink}
          onOpenLinkModal={(id) => {
            setLinkingSourceId(id);
            setIsLinkModalOpen(true);
          }}
        />
      </div>

      <NoteEditor
        isOpen={isEditorOpen}
        onClose={() => setIsEditorOpen(false)}
        onSave={handleSaveNote}
      />

      <ManualLinkModal
        isOpen={isLinkModalOpen}
        onClose={() => setIsLinkModalOpen(false)}
        currentNoteId={linkingSourceId}
        allNotes={allNotes}
        onConfirmLink={handleConfirmLink}
      />
    </div>
  );
}

export default App;

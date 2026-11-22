import React, { useState } from "react";
import ForceGraphView from "./ForceGraphView";
import WordConstellation from "./WordConstellation";
import RadialTreeView from "./RadialTreeView";

function GraphContainer({ graphData, onSelectNode, activeNodeId }) {
  const [activeTab, setActiveTab] = useState("radial"); // default to radial or user choice
  const [isFullScreen, setIsFullScreen] = useState(false);

  return (
    <div className={`viz-panel ${isFullScreen ? "fullscreen" : ""}`}>
      <div className="viz-toolbar">
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <span style={{ fontSize: "14px", fontWeight: "600", color: "#f8fafc" }}>
            Knowledge Explorer
          </span>
          <span style={{ fontSize: "11px", color: "#94a3b8" }}>
            ({graphData.nodes.length} nodes, {graphData.edges.length} links)
          </span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <div className="viz-tabs">
            <button
              className={`viz-tab-btn ${activeTab === "force" ? "active" : ""}`}
              onClick={() => setActiveTab("force")}
            >
              🕸️ Force Graph
            </button>
            <button
              className={`viz-tab-btn ${activeTab === "word" ? "active" : ""}`}
              onClick={() => setActiveTab("word")}
            >
              🌌 Word Constellation
            </button>
            <button
              className={`viz-tab-btn ${activeTab === "radial" ? "active" : ""}`}
              onClick={() => setActiveTab("radial")}
            >
              🎯 360° Radial Tree
            </button>
          </div>

          <button
            className="viz-tab-btn"
            style={{
              borderColor: isFullScreen ? "#06b6d4" : "#334155",
              color: isFullScreen ? "#06b6d4" : "#f1f5f9",
              background: isFullScreen ? "rgba(6, 182, 212, 0.15)" : "transparent",
            }}
            onClick={() => setIsFullScreen(!isFullScreen)}
            title="Toggle full screen view"
          >
            {isFullScreen ? "🗗 Exit Full View" : "⛶ Full View"}
          </button>
        </div>
      </div>

      <div className="viz-canvas-container">
        {activeTab === "force" && (
          <ForceGraphView
            graphData={graphData}
            onSelectNode={onSelectNode}
            activeNodeId={activeNodeId}
          />
        )}
        {activeTab === "word" && (
          <WordConstellation
            graphData={graphData}
            onSelectNode={onSelectNode}
            activeNodeId={activeNodeId}
          />
        )}
        {activeTab === "radial" && (
          <RadialTreeView
            graphData={graphData}
            onSelectNode={onSelectNode}
            activeNodeId={activeNodeId}
          />
        )}
      </div>

      <div
        style={{
          position: "absolute",
          bottom: "12px",
          left: "16px",
          fontSize: "11px",
          color: "#64748b",
          pointerEvents: "none",
          background: "rgba(15, 23, 42, 0.7)",
          padding: "4px 8px",
          borderRadius: "6px",
        }}
      >
        💡 Scroll mouse wheel to zoom in/out • Click and drag canvas to pan 360°
      </div>
    </div>
  );
}

export default GraphContainer;

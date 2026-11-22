import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const TAG_COLORS = {
  python: "#10b981",
  fastapi: "#06b6d4",
  ml: "#8b5cf6",
  "deep-learning": "#a855f7",
  ai: "#c084fc",
  nlp: "#ec4899",
  embeddings: "#f43f5e",
  "semantic-search": "#fb7185",
  database: "#f59e0b",
  sqlite: "#eab308",
  sql: "#f97316",
  frontend: "#38bdf8",
  react: "#60a5fa",
  javascript: "#3b82f6",
  graphs: "#6366f1",
  "knowledge-graph": "#818cf8",
  algorithms: "#4f46e5",
  physics: "#14b8a6",
  "quantum-ml": "#06b6d4",
  "neural-spiking": "#a855f7",
  "neuromorphic-hardware": "#ec4899",
  "quantum-algorithms": "#38bdf8",
  "qubit-states": "#06b6d4",
  "reinforcement-learning-policy": "#8b5cf6",
  "bioinformatics-genomics": "#10b981",
  "zero-knowledge-cryptography": "#f59e0b",
};

function getTagColor(tagName) {
  if (!tagName) return "#38bdf8";
  const clean = tagName.replace(/^#/, "").toLowerCase();
  for (const [key, color] of Object.entries(TAG_COLORS)) {
    if (clean.includes(key)) return color;
  }
  return "#06b6d4";
}

function RadialTreeView({ graphData, onSelectNode, activeNodeId }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!svgRef.current || !graphData || !graphData.nodes.length) return;

    const width = svgRef.current.clientWidth || 1000;
    const height = svgRef.current.clientHeight || 800;

    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3
      .select(svgRef.current)
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      .style("background", "radial-gradient(circle at center, #0f172a 0%, #070b14 100%)")
      .style("cursor", "grab");

    const g = svg.append("g");

    // Add D3 Zoom & Pan
    const zoom = d3
      .zoom()
      .scaleExtent([0.15, 3.5])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    svg.call(zoom);

    // Initial scale: wide-spread panoramic view
    svg.call(
      zoom.transform,
      d3.zoomIdentity.scale(0.58).translate(0, 0)
    );

    // 1. Group notes by primary tag
    const tagCluster = {};
    graphData.nodes.forEach((n) => {
      const primaryTag = (n.tags && n.tags[0]) || "general";
      if (!tagCluster[primaryTag]) tagCluster[primaryTag] = [];
      tagCluster[primaryTag].push(n);
    });

    const tagsList = Object.keys(tagCluster);
    const totalNotesCount = graphData.nodes.length;

    // WIDE SPREAD ORBITS: generous space between center, tags, and notes
    const rTags = 280;   // Wide inner ring for tags
    const rNotesBase = 560; // Wide outer ring for notes

    // Draw background concentric orbit guide rings
    const orbitGroup = g.append("g").attr("class", "orbit-rings").style("pointer-events", "none");
    [rTags, rNotesBase, rNotesBase + 90].forEach((r) => {
      orbitGroup
        .append("circle")
        .attr("r", r)
        .attr("fill", "none")
        .attr("stroke", "#1e293b")
        .attr("stroke-width", 1)
        .attr("stroke-dasharray", "4,8")
        .attr("opacity", 0.6);
    });

    // 2. Proportional Angular Distribution: tags with more notes get wider angular sectors
    let currentAngle = -Math.PI / 2;
    const tagPositions = [];
    const notePositions = [];
    const linkPaths = [];

    tagsList.forEach((tag) => {
      const notesInTag = tagCluster[tag];
      const noteCount = notesInTag.length;
      // Proportional angle span based on note count + baseline
      const angleSpan = ((noteCount + 1.2) / (totalNotesCount + tagsList.length * 1.2)) * (2 * Math.PI);
      const tagAngle = currentAngle + angleSpan / 2;

      const tx = rTags * Math.cos(tagAngle);
      const ty = rTags * Math.sin(tagAngle);
      const tagColor = getTagColor(tag);

      tagPositions.push({
        id: `tag-${tag}`,
        name: `#${tag}`,
        x: tx,
        y: ty,
        angle: tagAngle,
        color: tagColor,
      });

      // Link from Core to Tag
      linkPaths.push({
        source: { x: 0, y: 0 },
        target: { x: tx, y: ty },
        color: tagColor,
        isRootLink: true,
      });

      // Spread notes within this tag's sector
      notesInTag.forEach((note, noteIdx) => {
        let noteAngle;
        if (noteCount === 1) {
          noteAngle = tagAngle;
        } else {
          const step = (angleSpan * 0.85) / (noteCount - 1);
          noteAngle = currentAngle + (angleSpan * 0.075) + noteIdx * step;
        }

        // Multi-tier radial staggering: prevents overlapping horizontally
        const tierOffset = (noteIdx % 3) * 65;
        const currentRadius = rNotesBase + tierOffset;
        const nx = currentRadius * Math.cos(noteAngle);
        const ny = currentRadius * Math.sin(noteAngle);

        notePositions.push({
          id: note.id,
          title: note.title,
          x: nx,
          y: ny,
          color: tagColor,
        });

        // Curved Link from Tag to Note
        linkPaths.push({
          source: { x: tx, y: ty },
          target: { x: nx, y: ny },
          color: tagColor,
          isRootLink: false,
        });
      });

      currentAngle += angleSpan;
    });

    // 3. Draw Links
    const linkGroup = g.append("g").attr("class", "links");
    linkGroup
      .selectAll("path")
      .data(linkPaths)
      .join("path")
      .attr("d", (d) => {
        const midX = (d.source.x + d.target.x) / 2;
        const midY = (d.source.y + d.target.y) / 2;
        return `M${d.source.x},${d.source.y} Q${midX * 0.75},${midY * 0.75} ${d.target.x},${d.target.y}`;
      })
      .attr("fill", "none")
      .attr("stroke", (d) => d.color)
      .attr("stroke-opacity", (d) => (d.isRootLink ? 0.35 : 0.45))
      .attr("stroke-width", (d) => (d.isRootLink ? 1.5 : 2));

    // 4. Center Core
    const centerGroup = g.append("g").attr("class", "center-hub");
    centerGroup
      .append("circle")
      .attr("r", 40)
      .attr("fill", "none")
      .attr("stroke", "#3b82f6")
      .attr("stroke-width", 2)
      .attr("opacity", 0.4);

    centerGroup
      .append("circle")
      .attr("r", 30)
      .attr("fill", "url(#core-gradient)")
      .attr("filter", "drop-shadow(0 0 16px rgba(59, 130, 246, 0.7))");

    centerGroup
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "-4px")
      .attr("fill", "#ffffff")
      .attr("font-size", "11px")
      .attr("font-weight", "bold")
      .text("CORE");

    centerGroup
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "14px")
      .attr("fill", "#93c5fd")
      .attr("font-size", "10px")
      .text(`${graphData.nodes.length} Notes`);

    // 5. Draw Tags (Spacious, Clean Badges)
    const tagNodes = g
      .append("g")
      .attr("class", "tag-nodes")
      .selectAll("g")
      .data(tagPositions)
      .join("g")
      .attr("transform", (d) => `translate(${d.x}, ${d.y})`);

    tagNodes
      .append("rect")
      .attr("rx", 10)
      .attr("ry", 10)
      .attr("x", (d) => -Math.min(130, d.name.length * 4.2 + 14))
      .attr("y", -12)
      .attr("width", (d) => Math.min(260, d.name.length * 8.4 + 28))
      .attr("height", 24)
      .attr("fill", "#1e293b")
      .attr("stroke", (d) => d.color)
      .attr("stroke-width", 1.5)
      .attr("filter", (d) => `drop-shadow(0 0 8px ${d.color}40)`);

    tagNodes
      .append("circle")
      .attr("cx", (d) => -Math.min(130, d.name.length * 4.2 + 14) + 10)
      .attr("cy", 0)
      .attr("r", 4)
      .attr("fill", (d) => d.color);

    tagNodes
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dx", 6)
      .attr("dy", "0.35em")
      .attr("fill", "#f8fafc")
      .attr("font-size", "11px")
      .attr("font-weight", "600")
      .text((d) => d.name);

    // 6. Draw Note Cards (Wide-Spread Horizontal Cards)
    const noteNodes = g
      .append("g")
      .attr("class", "note-nodes")
      .selectAll("g")
      .data(notePositions)
      .join("g")
      .attr("transform", (d) => `translate(${d.x}, ${d.y})`)
      .style("cursor", "pointer")
      .on("click", (event, d) => onSelectNode(d.id));

    noteNodes
      .append("rect")
      .attr("rx", 8)
      .attr("ry", 8)
      .attr("x", (d) => (d.x >= 0 ? 10 : -Math.min(210, d.title.length * 6.8 + 26) - 10))
      .attr("y", -13)
      .attr("width", (d) => Math.min(210, d.title.length * 6.8 + 26))
      .attr("height", 26)
      .attr("fill", (d) => (d.id === activeNodeId ? "#1e293b" : "#0f172a"))
      .attr("stroke", (d) => (d.id === activeNodeId ? "#06b6d4" : "#334155"))
      .attr("stroke-width", (d) => (d.id === activeNodeId ? 2 : 1))
      .attr("filter", (d) =>
        d.id === activeNodeId
          ? "drop-shadow(0 0 12px #06b6d4)"
          : "drop-shadow(0 2px 6px rgba(0,0,0,0.6))"
      )
      .on("mouseenter", function (event, d) {
        d3.select(this)
          .attr("stroke", d.color)
          .attr("fill", "#1e293b")
          .attr("filter", `drop-shadow(0 0 12px ${d.color})`);
      })
      .on("mouseleave", function (event, d) {
        if (d.id !== activeNodeId) {
          d3.select(this)
            .attr("stroke", "#334155")
            .attr("fill", "#0f172a")
            .attr("filter", "drop-shadow(0 2px 6px rgba(0,0,0,0.6))");
        }
      });

    noteNodes
      .append("circle")
      .attr("cx", 0)
      .attr("cy", 0)
      .attr("r", (d) => (d.id === activeNodeId ? 6 : 4.5))
      .attr("fill", (d) => (d.id === activeNodeId ? "#ffffff" : d.color))
      .attr("stroke", (d) => d.color)
      .attr("stroke-width", 2);

    noteNodes
      .append("text")
      .attr("x", (d) => (d.x >= 0 ? 22 : -22))
      .attr("text-anchor", (d) => (d.x >= 0 ? "start" : "end"))
      .attr("dy", "0.35em")
      .attr("fill", (d) => (d.id === activeNodeId ? "#38bdf8" : "#e2e8f0"))
      .attr("font-size", "11px")
      .attr("font-weight", (d) => (d.id === activeNodeId ? "600" : "500"))
      .text((d) => (d.title.length > 26 ? d.title.slice(0, 24) + "…" : d.title))
      .style("pointer-events", "none");

    // Core Gradient
    const defs = svg.append("defs");
    const coreGrad = defs
      .append("radialGradient")
      .attr("id", "core-gradient")
      .attr("cx", "30%")
      .attr("cy", "30%");
    coreGrad.append("stop").attr("offset", "0%").attr("stop-color", "#38bdf8");
    coreGrad.append("stop").attr("offset", "100%").attr("stop-color", "#1d4ed8");
  }, [graphData, activeNodeId, onSelectNode]);

  return (
    <svg
      ref={svgRef}
      style={{
        width: "100%",
        height: "100%",
        display: "block",
        overflow: "hidden",
      }}
    />
  );
}

export default RadialTreeView;

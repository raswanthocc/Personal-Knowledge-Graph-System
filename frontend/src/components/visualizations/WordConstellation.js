import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

function WordConstellation({ graphData, onSelectNode, activeNodeId }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!svgRef.current || !graphData || !graphData.nodes.length) return;

    const width = svgRef.current.clientWidth || 900;
    const height = svgRef.current.clientHeight || 700;

    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3
      .select(svgRef.current)
      .attr("viewBox", [0, 0, width, height])
      .style("background", "radial-gradient(circle at center, #0f172a 0%, #070b14 100%)")
      .style("cursor", "grab");

    const g = svg.append("g");

    // Zoom behavior
    const zoom = d3
      .zoom()
      .scaleExtent([0.2, 3.5])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    svg.call(zoom);

    // Initial scale: wide spread view
    svg.call(
      zoom.transform,
      d3.zoomIdentity.translate(width * 0.15, height * 0.15).scale(0.7)
    );

    // Compute node degrees for sizing
    const degreeMap = {};
    graphData.edges.forEach((e) => {
      degreeMap[e.source] = (degreeMap[e.source] || 0) + 1;
      degreeMap[e.target] = (degreeMap[e.target] || 0) + 1;
    });

    const nodes = graphData.nodes.map((d) => ({
      ...d,
      degree: degreeMap[d.id] || 1,
    }));

    const links = graphData.edges.map((d) => ({
      source: d.source,
      target: d.target,
    }));

    // WIDE SPREAD FORCE SIMULATION (High repulsion, long links, collision avoidance)
    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d) => d.id)
          .distance(240)
      )
      .force("charge", d3.forceManyBody().strength(-1100))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force(
        "collision",
        d3.forceCollide().radius((d) => Math.max(55, d.title.length * 4.8))
      );

    // Draw link filaments (curved organic lines)
    const link = g
      .append("g")
      .selectAll("path")
      .data(links)
      .join("path")
      .attr("stroke", "#334155")
      .attr("stroke-opacity", 0.45)
      .attr("stroke-width", 1.5)
      .attr("fill", "none");

    // Draw word labels
    const node = g
      .append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .style("cursor", "pointer")
      .call(
        d3
          .drag()
          .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      )
      .on("click", (event, d) => onSelectNode(d.id));

    // Semi-transparent pill background to guarantee text is 100% readable without overlapping
    node
      .append("rect")
      .attr("rx", 6)
      .attr("ry", 6)
      .attr("x", (d) => -Math.min(180, d.title.length * 4.2 + 12))
      .attr("y", -11)
      .attr("width", (d) => Math.min(360, d.title.length * 8.4 + 24))
      .attr("height", 22)
      .attr("fill", (d) => (d.id === activeNodeId ? "rgba(6, 182, 212, 0.2)" : "rgba(15, 23, 42, 0.75)"))
      .attr("stroke", (d) => (d.id === activeNodeId ? "#06b6d4" : "rgba(51, 65, 85, 0.6)"))
      .attr("stroke-width", 1)
      .attr("filter", (d) => (d.id === activeNodeId ? "drop-shadow(0 0 8px #06b6d4)" : "none"));

    // Word text
    node
      .append("text")
      .text((d) => d.title)
      .attr("text-anchor", "middle")
      .attr("dy", ".35em")
      .attr("fill", (d) => (d.id === activeNodeId ? "#38bdf8" : "#f1f5f9"))
      .attr("font-size", (d) => `${Math.max(11, 10 + Math.min(6, d.degree))}px`)
      .attr("font-weight", (d) => (d.id === activeNodeId ? "bold" : "500"));

    simulation.on("tick", () => {
      link.attr("d", (d) => {
        const dx = d.target.x - d.source.x;
        const dy = d.target.y - d.source.y;
        const dr = Math.sqrt(dx * dx + dy * dy) * 1.5;
        return `M${d.source.x},${d.source.y}A${dr},${dr} 0 0,1 ${d.target.x},${d.target.y}`;
      });

      node.attr("transform", (d) => `translate(${d.x},${d.y})`);
    });

    return () => simulation.stop();
  }, [graphData, activeNodeId, onSelectNode]);

  return <svg ref={svgRef} style={{ width: "100%", height: "100%" }} />;
}

export default WordConstellation;

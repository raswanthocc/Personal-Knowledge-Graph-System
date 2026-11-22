import React, { useEffect, useRef } from "react";
import cytoscape from "cytoscape";

function ForceGraphView({ graphData, onSelectNode, activeNodeId }) {
  const containerRef = useRef(null);
  const cyRef = useRef(null);
  const layoutRef = useRef(null);

  // Initialize or update graph elements when graphData changes
  useEffect(() => {
    if (!containerRef.current || !graphData) return;

    const elements = [
      ...graphData.nodes.map((node) => ({
        data: {
          id: String(node.id),
          label: node.title,
          tags: node.tags.join(", "),
        },
      })),
      ...graphData.edges.map((edge, idx) => ({
        data: {
          id: `e-${edge.source}-${edge.target}-${idx}`,
          source: String(edge.source),
          target: String(edge.target),
        },
      })),
    ];

    // Safely stop any running layout before destroying
    if (layoutRef.current) {
      try {
        layoutRef.current.stop();
      } catch (e) {}
      layoutRef.current = null;
    }

    if (cyRef.current) {
      try {
        cyRef.current.destroy();
      } catch (e) {}
      cyRef.current = null;
    }

    const cy = cytoscape({
      container: containerRef.current,
      elements,
      userZoomingEnabled: true,
      userPanningEnabled: true,
      wheelSensitivity: 0.2,
      style: [
        {
          selector: "node",
          style: {
            "background-color": "#3b82f6",
            label: "data(label)",
            color: "#f8fafc",
            "font-size": "11px",
            "text-valign": "bottom",
            "text-margin-y": 6,
            width: 24,
            height: 24,
            "border-width": 2,
            "border-color": "#60a5fa",
          },
        },
        {
          selector: ".active-node",
          style: {
            "background-color": "#06b6d4",
            "border-color": "#ffffff",
            "border-width": 4,
            width: 32,
            height: 32,
            "font-size": "13px",
            "font-weight": "bold",
          },
        },
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#475569",
            "target-arrow-color": "#06b6d4",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            opacity: 0.8,
          },
        },
      ],
    });

    cy.on("tap", "node", (evt) => {
      const node = evt.target;
      onSelectNode(parseInt(node.id()));
    });

    cyRef.current = cy;

    // Run layout with wide-spread distribution and no overlapping
    const layout = cy.layout({
      name: "cose",
      animate: false,
      randomize: false,
      componentSpacing: 180,
      nodeOverlap: 60,
      nodeRepulsion: 1800000,
      idealEdgeLength: 160,
      edgeElasticity: 100,
      nestingFactor: 5,
      gravity: 80,
    });

    layoutRef.current = layout;
    layout.run();

    // Fit smoothly with padding so full network is panoramic
    cy.fit(null, 60);

    return () => {
      if (layoutRef.current) {
        try {
          layoutRef.current.stop();
        } catch (e) {}
        layoutRef.current = null;
      }
      if (cyRef.current) {
        try {
          cyRef.current.destroy();
        } catch (e) {}
        cyRef.current = null;
      }
    };
  }, [graphData, onSelectNode]);

  // Update selected node styling without destroying the graph instance
  useEffect(() => {
    if (!cyRef.current) return;
    try {
      cyRef.current.nodes().removeClass("active-node");
      if (activeNodeId) {
        const targetNode = cyRef.current.$(`node[id = "${activeNodeId}"]`);
        if (targetNode.length > 0) {
          targetNode.addClass("active-node");
        }
      }
    } catch (e) {}
  }, [activeNodeId]);

  return <div ref={containerRef} style={{ width: "100%", height: "100%" }} />;
}

export default ForceGraphView;

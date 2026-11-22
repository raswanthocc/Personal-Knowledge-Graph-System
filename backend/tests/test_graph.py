def test_graph_endpoint(client):
    client.post("/notes/", json={"title": "A", "content": "Node A [[B]]", "tags": ["graph-tag"]})
    client.post("/notes/", json={"title": "B", "content": "Node B"})

    graph_res = client.get("/graph/")
    assert graph_res.status_code == 200
    data = graph_res.json()
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) == 2
    # Verify edge exists
    edges = data["edges"]
    assert any(e["source"] == 1 and e["target"] == 2 for e in edges)

def test_graph_traversal_bfs_and_dfs(client):
    # Setup chain: Root -> Child 1 -> Grandchild
    #             Root -> Child 2
    r_res = client.post("/notes/", json={"title": "Root", "content": "Root links [[Child 1]] and [[Child 2]]", "tags": ["root-tag"]})
    assert r_res.status_code == 201
    r_id = r_res.json()["id"]

    c1_res = client.post("/notes/", json={"title": "Child 1", "content": "Links to [[Grandchild]]"})
    assert c1_res.status_code == 201
    c1_id = c1_res.json()["id"]

    c2_res = client.post("/notes/", json={"title": "Child 2", "content": "Leaf node"})
    assert c2_res.status_code == 201
    c2_id = c2_res.json()["id"]

    g_res = client.post("/notes/", json={"title": "Grandchild", "content": "Cyclic back to [[Root]]"})
    assert g_res.status_code == 201
    g_id = g_res.json()["id"]

    # 1. Test BFS Traversal
    bfs_res = client.get(f"/graph/traverse/{r_id}?method=bfs&max_depth=3")
    assert bfs_res.status_code == 200
    bfs_data = bfs_res.json()
    assert bfs_data["start_note_id"] == r_id
    assert bfs_data["method"] == "bfs"
    assert bfs_data["total_nodes_visited"] == 4
    # Root (0), Children (1), Grandchild (2)
    visited_ids = [n["id"] for n in bfs_data["visited_nodes"]]
    assert visited_ids[0] == r_id
    assert c1_id in visited_ids
    assert c2_id in visited_ids
    assert g_id in visited_ids

    # 2. Test Max Depth limit = 1
    depth1_res = client.get(f"/graph/traverse/{r_id}?method=bfs&max_depth=1")
    assert depth1_res.status_code == 200
    depth1_data = depth1_res.json()
    assert depth1_data["total_nodes_visited"] == 3  # Root + 2 children, grandchild is at depth 2
    assert g_id not in [n["id"] for n in depth1_data["visited_nodes"]]

    # 3. Test DFS Traversal
    dfs_res = client.get(f"/graph/traverse/{r_id}?method=dfs&max_depth=3")
    assert dfs_res.status_code == 200
    dfs_data = dfs_res.json()
    assert dfs_data["method"] == "dfs"
    assert dfs_data["total_nodes_visited"] == 4

    # 4. Test Traversal from non-existent note (404)
    nf_res = client.get("/graph/traverse/99999")
    assert nf_res.status_code == 404

    # 5. Test Incoming direction
    in_res = client.get(f"/graph/traverse/{g_id}?direction=incoming")
    assert in_res.status_code == 200
    in_data = in_res.json()
    assert in_data["start_note_id"] == g_id
    assert any(n["id"] == c1_id for n in in_data["visited_nodes"])

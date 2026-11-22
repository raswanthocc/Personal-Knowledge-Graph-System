def test_wiki_link_auto_resolution(client):
    # Create Target Note first
    client.post("/notes/", json={"title": "Note B", "content": "This is target note B."})

    # Create Source Note containing [[Note B]]
    res_a = client.post("/notes/", json={
        "title": "Note A",
        "content": "Referencing [[Note B]] inside content."
    })
    assert res_a.status_code == 201
    data_a = res_a.json()
    # Outgoing links of Note A should include Note B
    linked_titles = [l["title"] for l in data_a["linked_notes"]]
    assert "Note B" in linked_titles

    # Now inspect Note B - its backlinks must contain Note A!
    res_b = client.get("/notes/1")
    assert res_b.status_code == 200
    data_b = res_b.json()
    backlink_titles = [b["title"] for b in data_b["backlinks"]]
    assert "Note A" in backlink_titles

def test_forward_wiki_reference_resolution(client):
    # Note A is created before Note B exists, referencing [[Future Note]]
    client.post("/notes/", json={
        "title": "First Note",
        "content": "This mentions [[Future Note]] which is not created yet."
    })

    # Now create Future Note
    res_future = client.post("/notes/", json={
        "title": "Future Note",
        "content": "I was created later."
    })
    assert res_future.status_code == 201
    data_future = res_future.json()
    # Backlinks of Future Note should now automatically list First Note
    backlink_titles = [b["title"] for b in data_future["backlinks"]]
    assert "First Note" in backlink_titles

def test_unpredefined_bracket_tag_token_and_ranking(client):
    # 1. Existing Note on Machine Learning
    client.post("/notes/", json={
        "title": "Machine Learning Foundations",
        "content": "Supervised algorithms, gradient descent, and neural network optimization.",
        "tags": ["ml", "algorithms"]
    })

    # 2. New Note with brand new unpredefined bracketed tag: [[#deep-reinforcement]]
    res = client.post("/notes/", json={
        "title": "Reinforcement Policy Gradient",
        "content": "Optimizing neural policies using [[#deep-reinforcement]] learning.",
        "tags": []
    })
    assert res.status_code == 201
    data = res.json()

    # Verify the new tag was created dynamically
    assert "deep-reinforcement" in data["tags"]

    # Verify token & ranking auto-links to Machine Learning Foundations
    linked_titles = [l["title"] for l in data["linked_notes"]]
    assert "Machine Learning Foundations" in linked_titles

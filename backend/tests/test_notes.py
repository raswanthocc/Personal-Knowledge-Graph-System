def test_create_and_get_note(client):
    # 1. Create a note
    payload = {
        "title": "Introduction to Python",
        "content": "Python is dynamic and expressive.",
        "tags": ["Python", "#Programming", " backend "]
    }
    response = client.post("/notes/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Introduction to Python"
    assert data["content"] == "Python is dynamic and expressive."
    # Check normalized tags
    assert "python" in data["tags"]
    assert "programming" in data["tags"]
    assert "backend" in data["tags"]

    # 2. Get note by ID
    note_id = data["id"]
    get_res = client.get(f"/notes/{note_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == note_id

def test_filter_notes_by_tag_and_keyword(client):
    client.post("/notes/", json={"title": "Note 1", "content": "Alpha content", "tags": ["tagA"]})
    client.post("/notes/", json={"title": "Note 2", "content": "Beta content", "tags": ["tagB"]})
    client.post("/notes/", json={"title": "Note 3", "content": "Gamma content with keyword", "tags": ["tagA", "tagB"]})

    # Filter by tag
    res_tag = client.get("/notes/?tag=taga")
    assert res_tag.status_code == 200
    items = res_tag.json()
    assert len(items) == 2
    titles = [it["title"] for it in items]
    assert "Note 1" in titles
    assert "Note 3" in titles

    # Filter by keyword
    res_kw = client.get("/notes/?keyword=keyword")
    assert res_kw.status_code == 200
    kw_items = res_kw.json()
    assert len(kw_items) == 1
    assert kw_items[0]["title"] == "Note 3"

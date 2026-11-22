def test_reject_self_loop(client):
    res_a = client.post("/notes/", json={"title": "Single Note", "content": "No links yet."})
    note_id = res_a.json()["id"]

    # Try linking note to itself
    patch_res = client.patch(f"/notes/{note_id}/link", json={"target_id": note_id})
    assert patch_res.status_code == 400
    assert "Self-loops are not allowed" in patch_res.json()["detail"]

def test_reject_duplicate_link(client):
    res_1 = client.post("/notes/", json={"title": "Node 1", "content": "One"})
    res_2 = client.post("/notes/", json={"title": "Node 2", "content": "Two"})
    id_1 = res_1.json()["id"]
    id_2 = res_2.json()["id"]

    # First link succeeds
    link1 = client.patch(f"/notes/{id_1}/link", json={"target_id": id_2})
    assert link1.status_code == 200

    # Second link is rejected with 409 Conflict
    link2 = client.patch(f"/notes/{id_1}/link", json={"target_id": id_2})
    assert link2.status_code == 409

def test_reject_duplicate_title(client):
    client.post("/notes/", json={"title": "Unique Title", "content": "First"})
    dup_res = client.post("/notes/", json={"title": "Unique Title", "content": "Second"})
    assert dup_res.status_code == 409

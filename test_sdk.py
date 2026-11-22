import sys
import os

# Ensure knowledge_sdk can be imported
sys.path.insert(0, os.path.abspath("knowledge_sdk"))

from knowledge_sdk import ApiClient, Configuration
from knowledge_sdk.api.notes_api import NotesApi
from knowledge_sdk.api.graph_api import GraphApi
from knowledge_sdk.models.note_create import NoteCreate

def run_sdk_verification():
    print("========================================")
    print("Testing Platform SDK (knowledge_sdk)...")
    print("========================================")

    config = Configuration(host="http://localhost:8000")
    client = ApiClient(config)
    notes_api = NotesApi(client)
    graph_api = GraphApi(client)

    try:
        # 1. Fetch all notes
        notes = notes_api.get_notes_notes_get()
        print(f"[SDK SUCCESS] Successfully retrieved {len(notes)} notes from backend.")
        for n in notes[:3]:
            print(f"  - [{n.id}] {n.title} (Tags: {', '.join(n.tags)})")

        # 2. Get specific note detail
        if notes:
            first_id = notes[0].id
            detail = notes_api.get_note_by_id_notes_note_id_get(first_id)
            print(f"[SDK SUCCESS] Retrieved detail for Note '{detail.title}':")
            print(f"  - Outgoing Links: {len(detail.linked_notes)}")
            print(f"  - Backlinks: {len(detail.backlinks)}")

        # 3. Retrieve graph
        graph = graph_api.get_graph_graph_get()
        print(f"[SDK SUCCESS] Retrieved graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges.")

        # 4. Traverse graph via BFS
        if notes:
            traversal = graph_api.traverse_graph_graph_traverse_note_id_get(
                note_id=first_id,
                method="bfs",
                max_depth=2
            )
            print(f"[SDK SUCCESS] BFS Traversal from Note [{traversal.start_note_id}] '{traversal.start_note_title}':")
            print(f"  - Visited Nodes ({traversal.total_nodes_visited}): {traversal.traversal_order}")
            print(f"  - Edges Traversed: {len(traversal.edges)}")

        print("\nAll SDK tests passed successfully!")

    except Exception as e:
        print(f"[SDK ERROR] Could not connect or execute SDK call: {e}")
        print("Ensure FastAPI backend is running via `python main.py` at http://localhost:8000")

if __name__ == "__main__":
    run_sdk_verification()

# Personal Knowledge Graph System
### Full-Stack Knowledge Network with Bi-directional Linking, Graph Traversal & Platform SDK

A production-grade, full-stack Personal Knowledge Graph application built with **FastAPI**, **SQLite**, **Alembic**, and **ReactJS**. This system allows users to create notes, organize knowledge through normalized tags, traverse connections via outgoing links and backlinks, auto-resolve `[[Wiki Links]]`, explore graph topologies through three switchable visualization modes, and interact programmatically via an automatically generated **Python SDK**.

---

## ⚡ Quick Start: Installation & Setup

### Prerequisites
* **Python**: Version 3.10+ installed
* **Node.js**: Version 18+ and `npm` installed
* **Operating System**: Windows, macOS, or Linux

---

### Option A: Automated One-Click Setup (Recommended)

#### On Windows:
```bat
:: 1. Run the development setup script
setupdev.bat

:: 2. Start the full application (Backend on :8000, Frontend on :3000)
runapplication.bat
```

#### On macOS / Linux:
```bash
# 1. Make scripts executable and run setup
chmod +x setupdev.sh runapplication.sh
./setupdev.sh

# 2. Start the full application
./runapplication.sh
```

---

### Option B: Manual Step-by-Step Setup

#### 1. Backend Setup (FastAPI & SQLite)
```bash
# Create and activate Python virtual environment
python3 -m venv env
source env/bin/activate       # On Windows: call env\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Run database migrations with Alembic
alembic upgrade head

# (Optional) Seed the 20 initial interconnected notes
sqlite3 knowledge_graph.db < seed_data.sql

# Start the FastAPI backend server
python main.py
```
* Backend API runs at: **`http://localhost:8000`**
* Interactive Swagger UI documentation: **`http://localhost:8000/docs`**
* ReDoc documentation: **`http://localhost:8000/redoc`**

#### 2. Frontend Setup (ReactJS)
```bash
# In a separate terminal window:
cd frontend
npm install
npm start
```
* React Web Application opens automatically at: **`http://localhost:3000`**

---

### Running the Backend Unit Tests
The backend test suite runs with **pytest** against an in-memory SQLite database (`StaticPool`) ensuring complete isolation and millisecond execution:
```bash
# Run all unit tests
pytest backend/tests/
```
* **Result**: **10 / 10 tests pass (100% success rate)** across notes CRUD, wiki links, backlinks, validation, cycle handling, and BFS/DFS graph traversal.

---

### Running the Platform SDK Verification
The Python SDK in `./knowledge_sdk` was generated via OpenAPI Generator CLI. Verify its live communication against the running backend:
```bash
python test_sdk.py
```
* **Result**: Connects to `http://localhost:8000`, tests `NotesApi` (note listing, note details, backlinks) and `GraphApi` (graph topology, BFS traversal).

---

## 📡 REST API Endpoints Reference

All endpoints strictly follow REST conventions and return OpenAPI-compliant JSON payloads:

| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| **POST** | `/notes/` | Creates a new note, auto-resolves `[[Wiki Links]]`, registers dynamic tags, and applies token-ranking auto-linking. | `201 Created`, `409 Conflict`, `422 Validation Error` |
| **GET** | `/notes/` | Retrieves note summaries with optional query filters: `?tag=python` or `?keyword=async`. | `200 OK`, `422 Validation Error` |
| **GET** | `/notes/{note_id}` | Retrieves detailed note information including full content, `linked_notes` (outgoing), and `backlinks` (incoming). | `200 OK`, `404 Not Found` |
| **PATCH** | `/notes/{note_id}/link` | Manually establishes a directed link from `note_id` to `target_id`. Rejects self-loops and duplicate links. | `200 OK`, `400 Bad Request`, `404 Not Found`, `409 Conflict` |
| **GET** | `/graph/` | Returns the entire knowledge graph as `{ nodes: [...], edges: [...] }` for Cytoscape and D3. | `200 OK` |
| **GET** | `/graph/traverse/{note_id}` | Performs BFS or DFS graph traversal starting from `note_id` with `max_depth` (1-10) and `direction` (`outgoing`, `incoming`, `both`). | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **GET** | `/tags/suggestions/` | Returns autocomplete suggestions from existing normalized tags matching optional `?query=`. | `200 OK` |
| **GET** | `/tags/areas/` | Returns list of foundational technology domain areas for UI scoping dropdowns. | `200 OK` |
| **GET** | `/` | API health check returning service status and documentation links. | `200 OK` |

---

## 💾 Database Schema & Seed Corpus

SQLite database located at `./knowledge_graph.db` with relational foreign keys:

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE links (
    source_id INTEGER,
    target_id INTEGER,
    FOREIGN KEY (source_id) REFERENCES notes(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES notes(id) ON DELETE CASCADE,
    PRIMARY KEY (source_id, target_id)
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE note_tags (
    note_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (note_id, tag_id)
);
```

### Current Live Dataset (20 Notes, 42 Links, 27 Tags)
The database contains 20 curated, interconnected notes spanning six core computer science disciplines:
1. **Python Ecosystem:** Concurrency Models in Python, Pydantic Data Validation, Database Migrations with Alembic.
2. **FastAPI Architecture:** RESTful API Design Standards, API Contracts, Dependency Injection.
3. **Machine Learning & Deep Learning:** Neural Network Architectures, Transformer Attention Models, Large Language Model Foundations.
4. **NLP & Vector Embeddings:** Vector Distance & Cosine Metrics, Semantic Search.
5. **Database Systems & SQLite:** SQLite Pragma & Foreign Key Enforcement, Database Indexing & B-Trees.
6. **Frontend Architecture & React:** React Component Lifecycle, Axios Interceptors & Client State.
7. **Graph Theory & Knowledge Graphs:** Directed Acyclic Graphs (DAG), Backlink Indexing & Reverse Traversal.
8. **Advanced Frontiers:** Neuromorphic Computing & Spiking Hardware, Quantum Computing & Qubit Algorithms.

---

## 📦 Platform SDK Usage (`knowledge_sdk`)

The SDK is generated into `./knowledge_sdk`. Here is the exact usage pattern demonstrated in `test_sdk.py`:

```python
import sys
sys.path.insert(0, "knowledge_sdk")

from knowledge_sdk import ApiClient, Configuration
from knowledge_sdk.api.notes_api import NotesApi
from knowledge_sdk.api.graph_api import GraphApi

# Initialize client
config = Configuration(host="http://localhost:8000")
client = ApiClient(config)

notes_api = NotesApi(client)
graph_api = GraphApi(client)

# 1. Fetch all notes
notes = notes_api.get_notes_notes_get()
print(f"Total notes: {len(notes)}")

# 2. Get note detail with backlinks
detail = notes_api.get_note_by_id_notes_note_id_get(notes[0].id)
print(f"Note: {detail.title}")
print(f"Outgoing links: {len(detail.linked_notes)}, Backlinks: {len(detail.backlinks)}")

# 3. Retrieve graph topology
graph = graph_api.get_graph_graph_get()
print(f"Graph nodes: {len(graph.nodes)}, Edges: {len(graph.edges)}")

# 4. Traverse graph via BFS
traversal = graph_api.traverse_graph_graph_traverse_note_id_get(
    note_id=notes[0].id,
    method="bfs",
    max_depth=2
)
print(f"BFS Visited ({traversal.total_nodes_visited}): {traversal.traversal_order}")
```

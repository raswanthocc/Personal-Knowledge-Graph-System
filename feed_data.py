import httpx
import json

BASE_URL = "http://localhost:8000"

NOTES_TO_INSERT = [
    # 1-20: Interconnected Domain Notes
    {
        "title": "Concurrency Models in Python",
        "tags": ["python", "asyncio", "backend"],
        "content": "Python supports cooperative multitasking via asyncio. When designing async services in [[FastAPI Architecture]], the event loop handles multiple I/O requests concurrently without thread overhead, while data is persisted using non-blocking connections to [[Database Systems & SQLite]]."
    },
    {
        "title": "Pydantic Data Validation",
        "tags": ["python", "fastapi", "typing"],
        "content": "Pydantic enforces type hints at runtime in [[FastAPI Architecture]]. It validates incoming request schemas, coerces types, and automatically serializes database models into OpenAPI compliant JSON structures."
    },
    {
        "title": "Neural Network Architectures",
        "tags": ["ml", "deep-learning", "neural-networks"],
        "content": "Deep neural architectures use multilayer perceptrons, convolutional kernels, and recurrent connections. They are trained via gradient descent algorithms as introduced in [[Machine Learning & Deep Learning]], providing foundational representations for [[Transformer Attention Models]]."
    },
    {
        "title": "Transformer Attention Models",
        "tags": ["deep-learning", "nlp", "ai"],
        "content": "The self-attention mechanism computes query-key-value dot products, allowing models to weigh token relationships dynamically. This forms the backbone of modern LLMs discussed in [[NLP & Vector Embeddings]] and [[Large Language Model Foundations]]."
    },
    {
        "title": "Vector Distance & Cosine Metrics",
        "tags": ["nlp", "embeddings", "semantic-search"],
        "content": "Semantic similarity is evaluated by calculating the cosine distance between high-dimensional vector representations. This mathematical foundation powers document retrieval in [[NLP & Vector Embeddings]] and cluster node positioning in [[Graph Theory & Knowledge Graphs]]."
    },
    {
        "title": "Large Language Model Foundations",
        "tags": ["ai", "nlp", "deep-learning"],
        "content": "LLMs leverage massive parameter spaces pre-trained on diverse text corpora. They build on [[Transformer Attention Models]] and are exposed to users through modern APIs built with [[FastAPI Architecture]]."
    },
    {
        "title": "SQLite Pragma & Foreign Key Enforcement",
        "tags": ["database", "sqlite", "sql"],
        "content": "In SQLite, referential integrity requires executing PRAGMA foreign_keys = ON;. This guarantees cascaded deletions across association tables like note_tags and links as configured in [[Database Systems & SQLite]]."
    },
    {
        "title": "Database Indexing & B-Trees",
        "tags": ["database", "sql", "algorithms"],
        "content": "B-Tree indexes reduce table scan complexity from O(N) to O(log N). In our relational schema, unique indexes on note titles prevent duplicates and speed up lookup operations for [[SQLite Pragma & Foreign Key Enforcement]]."
    },
    {
        "title": "Database Migrations with Alembic",
        "tags": ["database", "python", "alembic"],
        "content": "Alembic provides schema version control for SQLAlchemy engines. It inspects metadata changes and applies revisions incrementally, ensuring database consistency for [[Database Systems & SQLite]] services."
    },
    {
        "title": "React Component Lifecycle",
        "tags": ["frontend", "react", "javascript"],
        "content": "React components manage mounting, updating, and unmounting phases using hooks like useEffect and useCallback. This lifecycle coordinates asynchronous data fetching from [[FastAPI Architecture]] services."
    },
    {
        "title": "Axios Interceptors & Client State",
        "tags": ["frontend", "react", "axios"],
        "content": "Axios instances configure base URLs, headers, and request interceptors. In our frontend, Axios calls fetch note details and knowledge network topologies from [[FastAPI Architecture]] to supply [[React Component Lifecycle]]."
    },
    {
        "title": "Directed Acyclic Graphs (DAG)",
        "tags": ["graphs", "algorithms", "data-structures"],
        "content": "A DAG represents directed relationships without circular loops. In our knowledge system, graph validation prevents self-loops and detects cycles during traversal as defined in [[Graph Theory & Knowledge Graphs]]."
    },
    {
        "title": "Backlink Indexing & Reverse Traversal",
        "tags": ["graphs", "knowledge-graph", "backlinks"],
        "content": "While forward links track target destinations, backlinks reveal incoming references. This bi-directional indexing enables associative note exploration, powering the relationship explorer in [[Frontend Architecture & React]]."
    },
    {
        "title": "Graph Force-Directed Layouts",
        "tags": ["graphs", "data-visualization", "cytoscape"],
        "content": "Force-directed algorithms simulate physical repulsion between nodes and spring-like attraction along edges. Cytoscape renders these physics equations to visualize [[Graph Theory & Knowledge Graphs]] in the browser."
    },
    {
        "title": "Circular Radial Dendrograms",
        "tags": ["graphs", "data-visualization", "d3"],
        "content": "Radial tree projections position hierarchical clusters along a 360-degree circular perimeter. Using D3, notes are nested under their normalized tag branches radiating from a central core in [[Frontend Architecture & React]]."
    },
    {
        "title": "Semantic Concept Constellations",
        "tags": ["graphs", "data-visualization", "nlp"],
        "content": "Word constellations render knowledge nodes as floating labels sized by connection degree. Curved Bezier links connect related terms, bridging visual analytics with [[Vector Distance & Cosine Metrics]]."
    },
    {
        "title": "RESTful API Design Standards",
        "tags": ["backend", "fastapi", "rest-api"],
        "content": "REST architectures adhere to stateless client-server contracts with standard HTTP status codes (201, 400, 404, 409). These endpoints connect frontend clients via [[Axios Interceptors & Client State]] to [[FastAPI Architecture]]."
    },
    {
        "title": "Python Typing & Metaclasses",
        "tags": ["python", "typing", "clean-code"],
        "content": "Python type annotations combined with runtime introspection allow frameworks like Pydantic and SQLAlchemy to build dynamic data mappers. This underlies [[Pydantic Data Validation]] in [[Python Ecosystem]]."
    },
    {
        "title": "Graph Search & Traversal Algorithms",
        "tags": ["graphs", "algorithms", "data-structures"],
        "content": "Breadth-First Search (BFS) and Depth-First Search (DFS) explore connected paths through adjacency lists. In a knowledge base, BFS uncovers multi-hop relationships between notes linked to [[Directed Acyclic Graphs (DAG)]]."
    },
    {
        "title": "Markdown AST & Inline Parsing",
        "tags": ["frontend", "markdown", "javascript"],
        "content": "Markdown text is tokenized into an Abstract Syntax Tree (AST). Regex parsers scan for wiki-style syntax [[Title]], transforming plain text into interactive navigation buttons inside [[React Component Lifecycle]]."
    },
    # 21-25: Notes with Brand New, Unpredefined Tags (Testing Token & Ranking Auto-Linker)
    {
        "title": "Neuromorphic Computing & Spiking Hardware",
        "tags": ["neuromorphic-hardware", "spiking-circuits"],
        "content": "Bio-inspired neuromorphic chips implement spiking neural architectures directly in silicon. They replace classical Von Neumann memory bottlenecks with artificial synapses that mimic deep neural network learning and gradient optimization."
    },
    {
        "title": "Quantum Computing & Qubit Algorithms",
        "tags": ["quantum-algorithms", "qubit-states"],
        "content": "Quantum computing leverages superposition and entanglement to execute parallel search algorithms. Quantum circuits process high-dimensional vector spaces and graph traversal operations that surpass classical limits."
    },
    {
        "title": "Reinforcement Learning Policy Gradients",
        "tags": ["reinforcement-learning-policy", "actor-critic"],
        "content": "Policy gradient methods optimize an agent's expected cumulative reward through neural network backpropagation. They combine deep neural networks with gradient descent algorithms for sequential decision tasks."
    },
    {
        "title": "Genomic Sequence Alignment",
        "tags": ["bioinformatics-genomics", "dna-sequencing"],
        "content": "Bioinformatics algorithms utilize dynamic programming and directed acyclic graph structures to align DNA and RNA sequences. High-dimensional vector embeddings are increasingly applied to classify protein structures."
    },
    {
        "title": "Zero Knowledge Proofs & Cryptographic Verification",
        "tags": ["zero-knowledge-cryptography", "zk-snarks"],
        "content": "Zero knowledge protocols allow one party to mathematically prove validation of database transactions without revealing sensitive content. These cryptographic state machines integrate into distributed database architectures for relational data integrity."
    }
]

def feed_data():
    print(f"Connecting to {BASE_URL} to insert {len(NOTES_TO_INSERT)} notes...")
    inserted_count = 0
    already_exist_count = 0

    client = httpx.Client(timeout=10.0)

    for note in NOTES_TO_INSERT:
        res = client.post(f"{BASE_URL}/notes/", json=note)
        if res.status_code == 201:
            data = res.json()
            inserted_count += 1
            print(f"[CREATED #{data['id']}] {data['title']} (Tags: {', '.join(data['tags'])}) -> Linked: {len(data['linked_notes'])}")
        elif res.status_code == 409:
            already_exist_count += 1
            print(f"[ALREADY EXISTS] {note['title']}")
        else:
            print(f"[ERROR {res.status_code}] Could not insert '{note['title']}': {res.text}")

    print("\n-------------------------------------------")
    print(f"Done! Inserted: {inserted_count}, Already existed: {already_exist_count}")

    # Fetch final graph summary
    graph_res = client.get(f"{BASE_URL}/graph/")
    if graph_res.status_code == 200:
        g = graph_res.json()
        print(f"Total graph now has {len(g['nodes'])} nodes and {len(g['edges'])} links!")

if __name__ == "__main__":
    feed_data()

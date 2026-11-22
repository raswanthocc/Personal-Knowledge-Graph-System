-- Enable SQLite Foreign Key Enforcement
PRAGMA foreign_keys = ON;

-- Clean existing data
DELETE FROM note_tags;
DELETE FROM links;
DELETE FROM tags;
DELETE FROM notes;

-- 1. Insert Initial Notes covering our 6 Interconnected Topics
INSERT INTO notes (id, title, content, created_at) VALUES
(1, 'Python Ecosystem', 'Python is a high-level programming language known for readability and clean syntax. Modern backend architectures frequently combine [[FastAPI Architecture]] for high performance APIs and asyncio for async I/O. Relational persistence is achieved through [[Database Systems & SQLite]].', '2026-11-20 10:00:00'),
(2, 'FastAPI Architecture', 'FastAPI is a modern web framework for Python based on Starlette and Pydantic. It provides automatic OpenAPI docs, dependency injection, and native async support. It integrates cleanly with [[Database Systems & SQLite]] and provides API contracts for [[Frontend Architecture & React]].', '2026-11-20 10:05:00'),
(3, 'Machine Learning & Deep Learning', 'Machine Learning enables computational systems to learn patterns from data without explicit programming. Deep Learning relies on deep neural networks and gradient optimization. Implementations commonly leverage [[Python Ecosystem]] and feed advanced representations into [[NLP & Vector Embeddings]].', '2026-11-20 10:10:00'),
(4, 'NLP & Vector Embeddings', 'Natural Language Processing converts text into dense vector representations. Using cosine similarity, semantic search can retrieve similar documents even without keyword overlap. These techniques are often represented as graph nodes in [[Graph Theory & Knowledge Graphs]].', '2026-11-20 10:15:00'),
(5, 'Database Systems & SQLite', 'SQLite is a serverless, self-contained, transactional SQL database engine. It supports ACID compliance, foreign keys via PRAGMA enforcement, and indexing. Schema versions are maintained with Alembic, powering backend services in [[FastAPI Architecture]].', '2026-11-20 10:20:00'),
(6, 'Frontend Architecture & React', 'React is a component-driven declarative JavaScript library for user interfaces. It communicates with the backend via Axios, renders markdown syntax, and visualizes relational networks using Cytoscape or D3 as documented in [[Graph Theory & Knowledge Graphs]].', '2026-11-20 10:25:00'),
(7, 'Graph Theory & Knowledge Graphs', 'A Knowledge Graph represents entities as nodes and relationships as edges. By analyzing directed acyclic structures and backlinks, users can traverse complex knowledge networks. Visual interactive explorers are rendered in [[Frontend Architecture & React]].', '2026-11-20 10:30:00');

-- 2. Insert Normalized Tags
INSERT INTO tags (id, name) VALUES
(1, 'python'),
(2, 'fastapi'),
(3, 'backend'),
(4, 'ml'),
(5, 'deep-learning'),
(6, 'ai'),
(7, 'nlp'),
(8, 'embeddings'),
(9, 'semantic-search'),
(10, 'database'),
(11, 'sqlite'),
(12, 'sql'),
(13, 'frontend'),
(14, 'react'),
(15, 'javascript'),
(16, 'graphs'),
(17, 'knowledge-graph'),
(18, 'algorithms');

-- 3. Associate Notes with Tags (note_tags)
INSERT INTO note_tags (note_id, tag_id) VALUES
-- Python Ecosystem (1)
(1, 1), (1, 3),
-- FastAPI Architecture (2)
(2, 1), (2, 2), (2, 3),
-- Machine Learning & Deep Learning (3)
(3, 4), (3, 5), (3, 6),
-- NLP & Vector Embeddings (4)
(4, 6), (4, 7), (4, 8), (4, 9),
-- Database Systems & SQLite (5)
(5, 3), (5, 10), (5, 11), (5, 12),
-- Frontend Architecture & React (6)
(6, 13), (6, 14), (6, 15),
-- Graph Theory & Knowledge Graphs (7)
(7, 16), (7, 17), (7, 18);

-- 4. Insert Directed Graph Links (Explicit and Wiki Auto-Links)
INSERT INTO links (source_id, target_id) VALUES
-- Note 1 -> Note 2 (FastAPI), Note 1 -> Note 5 (SQLite)
(1, 2),
(1, 5),
-- Note 2 -> Note 5 (SQLite), Note 2 -> Note 6 (React)
(2, 5),
(2, 6),
-- Note 3 -> Note 1 (Python), Note 3 -> Note 4 (NLP)
(3, 1),
(3, 4),
-- Note 4 -> Note 7 (Graphs)
(4, 7),
-- Note 5 -> Note 2 (FastAPI)
(5, 2),
-- Note 6 -> Note 7 (Graphs)
(6, 7),
-- Note 7 -> Note 6 (React)
(7, 6);

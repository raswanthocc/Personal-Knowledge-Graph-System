from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import Base, engine
from backend.app.routers import notes, graph, tags

# Create tables if not existing
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Knowledge Graph API",
    description="API for bi-directionally linking notes, backlinks, graph traversal, and tag-based knowledge discovery.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Notes", "description": "Operations with notes and links"},
        {"name": "Graph", "description": "Graph topology and traversal"},
        {"name": "Tags", "description": "Tag normalization and suggestions"}
    ]
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router)
app.include_router(graph.router)
app.include_router(tags.router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": "Personal Knowledge Graph API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

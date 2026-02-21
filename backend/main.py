from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

from api import routes_collections, routes_documents, routes_chat

app = FastAPI(
    title="RAG Application API",
    description="API for managing Qdrant collections, uploading documents, and RAG chat.",
    version="1.0.0",
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_collections.router)
app.include_router(routes_documents.router)
app.include_router(routes_chat.router)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Backend API is running"}

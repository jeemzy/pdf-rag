"""
Branch 1: Vectorize Documents
- Parse PDFs
- Semantic chunking via langchain
- Generate OpenAI embeddings
- Insert into Qdrant vector store
"""

import os
from pathlib import Path

from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http import models
import uuid

import config


def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from a PDF file, joining pages."""
    reader = PdfReader(file_path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def chunk_text(text: str, embeddings: OpenAIEmbeddings) -> list[str]:
    """Split text into semantic chunks using langchain SemanticChunker."""
    splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type=config.CHUNK_BREAKPOINT_THRESHOLD_TYPE,
    )
    documents = splitter.create_documents([text])

    # Filter chunks by size constraints
    chunks = []
    for doc in documents:
        content = doc.page_content.strip()
        if len(content) < config.CHUNK_MIN_SIZE:
            continue
        if len(content) > config.CHUNK_MAX_SIZE:
            # Split oversized chunks naively at max_size boundaries
            for i in range(0, len(content), config.CHUNK_MAX_SIZE):
                sub = content[i : i + config.CHUNK_MAX_SIZE].strip()
                if len(sub) >= config.CHUNK_MIN_SIZE:
                    chunks.append(sub)
        else:
            chunks.append(content)

    return chunks


def ensure_collection(client: QdrantClient, collection_name: str, vector_size: int):
    """Create Qdrant collection if it does not exist."""
    collections = [c.name for c in client.get_collections().collections]
    if collection_name not in collections:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )
        print(f"  Created Qdrant collection: {collection_name}")


def process(file_paths: list[str]):
    """Process a list of PDF files: chunk, embed, and insert into Qdrant."""
    print("\n=== Branch 1: Vectorize Documents ===")

    # Validate API key
    api_key = config.OPENAI_API_KEY
    if api_key.startswith("PLACEHOLDER"):
        print("ERROR: Set OPENAI_API_KEY environment variable before running.")
        return

    if config.QDRANT_HOST.startswith("PLACEHOLDER"):
        print("ERROR: Set QDRANT_HOST in config.py before running.")
        return

    if config.QDRANT_API_KEY.startswith("PLACEHOLDER"):
        print("ERROR: Set QDRANT_API_KEY in config.py before running.")
        return

    # Initialize clients
    embeddings = OpenAIEmbeddings(api_key=api_key)
    qdrant = QdrantClient(
        url=f"http://{config.QDRANT_HOST}:{config.QDRANT_PORT}",
        api_key=config.QDRANT_API_KEY,
    )

    total_chunks = 0

    for file_path in file_paths:
        file_name = Path(file_path).name
        print(f"\nProcessing: {file_name}")

        # 0. Delete existing document chunks (if any)
        try:
            print(f"  Removing previous data for '{file_name}' from Qdrant (if any)...")
            qdrant.delete(
                collection_name=config.QDRANT_COLLECTION,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="metadata.document_name",
                                match=models.MatchValue(value=file_name),
                            ),
                        ],
                    )
                ),
            )
        except Exception as e:
            print(f"  WARNING: Could not delete existing document data. ({e})")

        # 1. Extract text
        text = extract_text_from_pdf(file_path)
        if not text.strip():
            print(f"  WARNING: No text extracted from {file_name}, skipping.")
            continue
        print(f"  Extracted {len(text)} characters")

        # 2. Chunk
        chunks = chunk_text(text, embeddings)
        print(f"  Split into {len(chunks)} chunks")

        if not chunks:
            print(f"  WARNING: No valid chunks for {file_name}, skipping.")
            continue

        # 3. Embed
        print(f"  Generating embeddings...")
        vectors = embeddings.embed_documents(chunks)
        vector_size = len(vectors[0])

        # 4. Ensure collection exists
        ensure_collection(qdrant, config.QDRANT_COLLECTION, vector_size)

        # 5. Insert into Qdrant
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "pageContent": chunk,     # Langchain JS in-memory
                    "page_content": chunk,    # Langchain Python/JS standard
                    "content": chunk,         # n8n Qdrant node default
                    "text": chunk,            # legacy default
                    "metadata": {
                        "document_name": file_name,
                        "chunk_index": i,
                    },
                },
            )
            for i, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]

        qdrant.upsert(
            collection_name=config.QDRANT_COLLECTION,
            points=points,
        )
        total_chunks += len(points)
        print(f"  Inserted {len(points)} vectors into Qdrant")

    print(f"\nDone. Total vectors inserted: {total_chunks}")

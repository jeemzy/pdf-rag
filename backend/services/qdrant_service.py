import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    FilterSelector,
    Filter,
    FieldCondition,
    MatchValue,
)
from core.config import settings


class QdrantService:
    def __init__(self):
        self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

    def get_collections(self):
        """List all Qdrant collections."""
        collections = self.client.get_collections().collections
        return [c.name for c in collections]

    def ensure_collection(self, collection_name: str, vector_size: int = 1536):
        """Create Qdrant collection if it does not exist."""
        collections = self.get_collections()
        if collection_name not in collections:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )
            return {"status": "created", "name": collection_name}
        return {"status": "exists", "name": collection_name}

    def delete_collection(self, collection_name: str):
        """Delete a collection entirely."""
        self.client.delete_collection(collection_name)

    def delete_document_chunks(self, collection_name: str, document_name: str):
        """Delete chunks pertaining to a specific document."""
        self.client.delete(
            collection_name=collection_name,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="metadata.document_name",
                            match=MatchValue(value=document_name),
                        ),
                    ],
                )
            ),
        )

    def upsert_vectors(
        self,
        collection_name: str,
        chunks: list[str],
        vectors: list[list[float]],
        document_name: str,
    ):
        """Upsert embedded chunks into Qdrant."""
        if not chunks or not vectors:
            return 0

        vector_size = len(vectors[0])
        self.ensure_collection(collection_name, vector_size)

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "page_content": chunk,
                    "metadata": {
                        "document_name": document_name,
                        "chunk_index": i,
                    },
                },
            )
            for i, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]

        self.client.upsert(
            collection_name=collection_name,
            points=points,
        )
        return len(points)


qdrant_service = QdrantService()

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.qdrant_service import qdrant_service

router = APIRouter(prefix="/collections", tags=["Collections"])


class CollectionCreate(BaseModel):
    name: str
    vector_size: int = 1536


class CollectionDelete(BaseModel):
    name: str


@router.get("/")
def list_collections():
    """List all available Qdrant collections."""
    try:
        collections = qdrant_service.get_collections()
        return {"collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_collection(collection: CollectionCreate):
    """Ensure a Qdrant collection exists."""
    try:
        result = qdrant_service.ensure_collection(
            collection.name, collection.vector_size
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{collection_name}")
def delete_collection(collection_name: str):
    """Delete a specific collection."""
    try:
        qdrant_service.delete_collection(collection_name)
        return {"status": "deleted", "name": collection_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

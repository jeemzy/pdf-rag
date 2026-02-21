from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag_service import rag_service

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    collection_name: str
    message: str


class ChatResponse(BaseModel):
    answer: str
    context: list[str]


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Generate an answer using RAG for a given collection and question."""
    try:
        response = rag_service.get_answer(
            collection_name=request.collection_name, query=request.message
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

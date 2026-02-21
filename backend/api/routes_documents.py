from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from services.rag_service import rag_service
from services.qdrant_service import qdrant_service

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    collection_name: str = Form(...), file: UploadFile = File(...)
):
    """Upload a PDF document, chunk it, embed it, and store in Qdrant collection."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        content = await file.read()

        # 1. Clean up old chunks for this document to avoid duplicates
        try:
            qdrant_service.delete_document_chunks(collection_name, file.filename)
        except Exception:
            pass  # Collection might not exist yet

        # 2. Process and insert the new document
        num_inserted = rag_service.process_document(
            collection_name=collection_name,
            document_name=file.filename,
            pdf_bytes=content,
        )

        return {
            "status": "success",
            "message": f"Successfully processed {file.filename}.",
            "chunks_inserted": num_inserted,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

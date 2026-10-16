from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document
from app.schemas.extraction import ExtractRequest
from app.ai.extractor import extractor_service

router = APIRouter(prefix="/extract", tags=["Extraction"])

@router.post("")
async def extract_structured_data(
    payload: ExtractRequest,
    db: Session = Depends(get_db)
):
    """
    Triggers structured schema extraction from document text.
    Target types: invoice, contract, resume, generic, or custom schema prompt.
    """
    doc = db.query(Document).filter(Document.id == payload.document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    target_type = payload.target_type or doc.classification or "general"
    
    result = await extractor_service.extract(
        text=doc.raw_text or "",
        document_type=target_type,
        custom_prompt=payload.custom_schema_prompt
    )

    # Cache extracted data onto the document record
    doc.extracted_data = result.get("data", {})
    db.commit()

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "target_type": target_type,
        "extracted_data": doc.extracted_data,
        "model_used": result.get("model_used"),
        "is_mock": result.get("is_mock", False)
    }

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document, ComparisonRecord
from app.schemas.comparison import CompareRequest, CompareResponse
from app.ai.comparator import comparator_service

router = APIRouter(prefix="/compare", tags=["Comparison"])

@router.post("", response_model=CompareResponse)
async def compare_documents(
    payload: CompareRequest,
    db: Session = Depends(get_db)
):
    """
    Compares two documents or contract versions, outputting clause divergences,
    added/modified terms, and risk evaluations.
    """
    doc_a = db.query(Document).filter(Document.id == payload.doc_a_id).first()
    doc_b = db.query(Document).filter(Document.id == payload.doc_b_id).first()

    if not doc_a or not doc_b:
        raise HTTPException(status_code=404, detail="One or both documents not found")

    result = await comparator_service.compare(
        doc_a_name=doc_a.filename,
        doc_a_text=doc_a.raw_text or "",
        doc_b_name=doc_b.filename,
        doc_b_text=doc_b.raw_text or ""
    )

    comparison = ComparisonRecord(
        id=str(uuid.uuid4()),
        doc_a_id=doc_a.id,
        doc_b_id=doc_b.id,
        doc_a_name=doc_a.filename,
        doc_b_name=doc_b.filename,
        diff_summary=result["diff_summary"],
        clauses_comparison=result["clauses_comparison"],
        risk_assessment=result["risk_assessment"]
    )
    db.add(comparison)
    db.commit()
    db.refresh(comparison)

    return comparison

@router.get("/history")
def list_comparisons(db: Session = Depends(get_db)):
    """List recent comparison records."""
    records = db.query(ComparisonRecord).order_by(ComparisonRecord.created_at.desc()).limit(20).all()
    return records

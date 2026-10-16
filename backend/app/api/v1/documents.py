import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.models.document import Document, DocumentChunk
from app.schemas.document import DocumentResponse, DocumentDetailResponse, DocumentChunkResponse
from app.services.document_parser import document_parser
from app.services.sample_data import SAMPLE_DOCUMENTS
from app.ai.classifier import classifier_service
from app.ai.summarizer import summarizer_service
from app.ai.extractor import extractor_service
from app.ai.embeddings import embedding_engine

router = APIRouter(prefix="/documents", tags=["Documents"])

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.get("", response_model=List[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    """List all ingested documents with chunks count and classification."""
    docs = db.query(Document).order_by(Document.created_at.desc()).all()
    results = []
    for d in docs:
        item = DocumentResponse.model_validate(d)
        item.chunks_count = len(d.chunks)
        results.append(item)
    return results

@router.get("/{document_id}", response_model=DocumentDetailResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    """Retrieve full document details and chunk passages."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    resp = DocumentDetailResponse.model_validate(doc)
    resp.chunks_count = len(doc.chunks)
    resp.chunks = [DocumentChunkResponse.model_validate(c) for c in doc.chunks]
    return resp

@router.post("/upload", response_model=DocumentDetailResponse)
async def upload_document(
    file: UploadFile = File(...),
    auto_analyze: bool = Form(True),
    db: Session = Depends(get_db)
):
    """
    Upload a document (PDF, DOCX, TXT, MD), parse text, compute embeddings,
    and optionally trigger autonomous classification and summary.
    """
    file_bytes = await file.read()
    file_size = len(file_bytes)
    
    if file_size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File exceeds maximum limit of {settings.MAX_FILE_SIZE_MB}MB")

    ext = os.path.splitext(file.filename)[1].lower().replace(".", "")
    if ext not in ["pdf", "docx", "doc", "txt", "md"]:
        raise HTTPException(status_code=400, detail="Supported file formats: PDF, DOCX, TXT, MD")

    file_id = str(uuid.uuid4())
    saved_filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, saved_filename)
    
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Parse and chunk document
    raw_text, chunks_data = document_parser.extract_text_and_chunks(file_bytes, ext)

    doc = Document(
        id=file_id,
        filename=file.filename,
        file_type=ext,
        file_size=file_size,
        file_path=file_path,
        raw_text=raw_text,
        status="processing"
    )
    db.add(doc)
    db.flush()

    # Save chunks with decoupled embeddings
    for c in chunks_data:
        chunk_obj = DocumentChunk(
            id=str(uuid.uuid4()),
            document_id=doc.id,
            chunk_index=c["chunk_index"],
            content=c["content"],
            page_number=c["page_number"],
            token_count=c["token_count"],
            embedding=c["embedding"]
        )
        db.add(chunk_obj)

    db.commit()

    # Autonomous analysis if requested
    if auto_analyze and raw_text.strip():
        try:
            # 1. Classification
            cls_result = await classifier_service.classify(raw_text, file.filename)
            doc.classification = cls_result["category"]
            doc.classification_confidence = cls_result["confidence"]
            doc.classification_reason = cls_result["reason"]
            doc.classification_metadata = cls_result["metadata"]

            # 2. Structured Extraction based on category
            ext_result = await extractor_service.extract(raw_text, doc.classification)
            doc.extracted_data = ext_result.get("data", {})

            # 3. Summarization
            sum_result = await summarizer_service.summarize(raw_text, file.filename)
            doc.summary = sum_result

            doc.status = "ready"
            db.commit()
        except Exception as e:
            doc.status = "ready"
            db.commit()

    db.refresh(doc)
    return get_document(doc.id, db)

@router.delete("/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Delete a document and all related vector chunks."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if doc.file_path and os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception:
            pass

    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully", "id": document_id}

@router.post("/seed", response_model=List[DocumentResponse])
def seed_sample_documents(db: Session = Depends(get_db)):
    """Seed high-value sample enterprise documents for instant demo & testing."""
    for s in SAMPLE_DOCUMENTS:
        existing = db.query(Document).filter(Document.id == s["id"]).first()
        if not existing:
            doc = Document(
                id=s["id"],
                filename=s["filename"],
                file_type=s["file_type"],
                file_size=s["file_size"],
                raw_text=s["raw_text"],
                classification=s["classification"],
                classification_confidence=s["classification_confidence"],
                classification_reason=s["classification_reason"],
                classification_metadata=s["classification_metadata"],
                extracted_data=s["extracted_data"],
                summary=s["summary"],
                status="ready"
            )
            db.add(doc)
            db.flush()

            # Create chunks with embeddings
            paragraphs = [p for p in s["raw_text"].split("\n\n") if p.strip()]
            for idx, p in enumerate(paragraphs):
                emb = embedding_engine.embed_text(p)
                chunk_obj = DocumentChunk(
                    id=str(uuid.uuid4()),
                    document_id=doc.id,
                    chunk_index=idx,
                    content=p,
                    page_number=1,
                    token_count=len(p.split()),
                    embedding=emb
                )
                db.add(chunk_obj)
    
    db.commit()
    return list_documents(db)

import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document, DocumentChunk, ChatMessage
from app.schemas.chat import ChatRequest, ChatResponse
from app.ai.rag import rag_service

router = APIRouter(prefix="/chat", tags=["RAG Chat"])

@router.post("", response_model=ChatResponse)
async def chat_with_document(
    payload: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Retrieves grounded semantic chunks and generates citation-backed answers via OpenRouter.
    """
    chunks = []
    if payload.document_id:
        doc = db.query(Document).filter(Document.id == payload.document_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        chunks = doc.chunks
    else:
        # Cross-document workspace RAG query
        chunks = db.query(DocumentChunk).limit(100).all()

    if not chunks:
        raise HTTPException(status_code=400, detail="No document passages available for search. Please upload a document first.")

    # Save user message
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        document_id=payload.document_id,
        role="user",
        content=payload.message,
        created_at=datetime.utcnow()
    )
    db.add(user_msg)

    # Perform grounded RAG
    rag_result = await rag_service.answer_question(
        query=payload.message,
        chunks=chunks,
        model=payload.model
    )

    assistant_msg = ChatMessage(
        id=str(uuid.uuid4()),
        document_id=payload.document_id,
        role="assistant",
        content=rag_result["content"],
        citations=rag_result["citations"],
        model_used=rag_result["model_used"],
        created_at=datetime.utcnow()
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    return assistant_msg

@router.get("/history/{document_id}")
def get_chat_history(document_id: str, db: Session = Depends(get_db)):
    """Fetch previous conversation history for a specific document."""
    messages = db.query(ChatMessage).filter(
        ChatMessage.document_id == document_id
    ).order_by(ChatMessage.created_at.asc()).all()
    return messages

@router.post("/stream")
async def stream_chat(
    payload: ChatRequest,
    db: Session = Depends(get_db)
):
    """Streams RAG completion tokens via SSE."""
    chunks = []
    if payload.document_id:
        doc = db.query(Document).filter(Document.id == payload.document_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        chunks = doc.chunks
    else:
        chunks = db.query(DocumentChunk).limit(100).all()

    async def event_generator():
        async for token in rag_service.stream_answer_question(
            query=payload.message,
            chunks=chunks,
            model=payload.model
        ):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

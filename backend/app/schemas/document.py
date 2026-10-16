from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class DocumentChunkResponse(BaseModel):
    id: str
    chunk_index: int
    content: str
    page_number: int
    token_count: int

    class Config:
        from_attributes = True

class DocumentClassificationResponse(BaseModel):
    category: str
    confidence: float
    reason: str
    metadata: Dict[str, Any] = {}

class DocumentSummaryResponse(BaseModel):
    executive: str
    bullets: List[str]
    tldr: str
    action_items: List[str] = []

class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    raw_text: Optional[str] = None
    classification: str
    classification_confidence: float
    classification_reason: Optional[str] = None
    classification_metadata: Optional[Dict[str, Any]] = None
    extracted_data: Optional[Dict[str, Any]] = None
    summary: Optional[Dict[str, Any]] = None
    status: str
    created_at: datetime
    updated_at: datetime
    chunks_count: Optional[int] = 0

    class Config:
        from_attributes = True

class DocumentDetailResponse(DocumentResponse):
    chunks: List[DocumentChunkResponse] = []

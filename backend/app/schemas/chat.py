from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CitationItem(BaseModel):
    chunk_id: str
    chunk_index: int
    page_number: int
    snippet: str
    relevance_score: float

class ChatRequest(BaseModel):
    document_id: Optional[str] = None
    message: str
    model: Optional[str] = None
    stream: bool = False

class ChatResponse(BaseModel):
    id: str
    document_id: Optional[str] = None
    role: str
    content: str
    citations: List[CitationItem] = []
    model_used: str
    created_at: datetime

    class Config:
        from_attributes = True

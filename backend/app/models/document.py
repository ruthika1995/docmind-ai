import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)  # pdf, docx, txt, md
    file_size = Column(Integer, nullable=False)
    file_path = Column(String(512), nullable=True)
    raw_text = Column(Text, nullable=True)
    
    # Document Classification
    classification = Column(String(50), default="general") # invoice, contract, resume, financial_report, research_paper, general
    classification_confidence = Column(Float, default=0.0)
    classification_reason = Column(Text, nullable=True)
    classification_metadata = Column(JSON, default=dict)
    
    # Extracted Structured Data (JSON Schema)
    extracted_data = Column(JSON, default=dict)
    
    # Multi-Format Summaries
    summary = Column(JSON, default=dict) # {"executive": "...", "bullets": [...], "tldr": "...", "action_items": [...]}
    
    status = Column(String(30), default="ready") # uploaded, processing, ready, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    page_number = Column(Integer, default=1)
    token_count = Column(Integer, default=0)
    embedding = Column(JSON, nullable=True) # List of floats
    
    document = relationship("Document", back_populates="chunks")

class ComparisonRecord(Base):
    __tablename__ = "comparisons"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    doc_a_id = Column(String(36), nullable=False)
    doc_b_id = Column(String(36), nullable=False)
    doc_a_name = Column(String(255), nullable=False)
    doc_b_name = Column(String(255), nullable=False)
    
    diff_summary = Column(Text, nullable=False)
    clauses_comparison = Column(JSON, default=list) # [{ clause_name, doc_a_text, doc_b_text, change_type, risk_level, notes }]
    risk_assessment = Column(JSON, default=dict) # { overall_risk, risk_factors, recommendations }
    
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=True)
    role = Column(String(20), nullable=False) # user, assistant, system
    content = Column(Text, nullable=False)
    citations = Column(JSON, default=list) # [{ chunk_id, page_number, snippet, relevance_score }]
    model_used = Column(String(100), default="openrouter")
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="chat_messages")

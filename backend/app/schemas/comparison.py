from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ClauseDifference(BaseModel):
    clause_name: str
    doc_a_text: str
    doc_b_text: str
    change_type: str # added, removed, modified, unchanged
    risk_level: str  # low, medium, high
    notes: str

class CompareRequest(BaseModel):
    doc_a_id: str
    doc_b_id: str

class CompareResponse(BaseModel):
    id: str
    doc_a_id: str
    doc_b_id: str
    doc_a_name: str
    doc_b_name: str
    diff_summary: str
    clauses_comparison: List[ClauseDifference]
    risk_assessment: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

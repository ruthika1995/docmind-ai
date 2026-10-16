from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class InvoiceLineItem(BaseModel):
    description: str
    quantity: float = 1.0
    unit_price: float = 0.0
    total: float = 0.0

class InvoiceExtraction(BaseModel):
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    due_date: Optional[str] = None
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    line_items: List[InvoiceLineItem] = []
    subtotal: Optional[float] = 0.0
    tax: Optional[float] = 0.0
    total_amount: Optional[float] = 0.0
    currency: str = "USD"
    payment_terms: Optional[str] = None

class ContractExtraction(BaseModel):
    title: Optional[str] = None
    parties: List[str] = []
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None
    governing_law: Optional[str] = None
    key_obligations: List[str] = []
    payment_terms: Optional[str] = None
    termination_clause: Optional[str] = None
    liability_cap: Optional[str] = None
    confidentiality_period: Optional[str] = None
    auto_renewal: bool = False

class ResumeExperienceItem(BaseModel):
    company: str
    role: str
    duration: Optional[str] = None
    highlights: List[str] = []

class ResumeExtraction(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    skills: Dict[str, List[str]] = Field(default_factory=dict)
    experience: List[ResumeExperienceItem] = []
    education: List[Dict[str, Any]] = []
    certifications: List[str] = []

class GenericExtraction(BaseModel):
    title: Optional[str] = None
    document_date: Optional[str] = None
    author: Optional[str] = None
    organization: Optional[str] = None
    entities: List[Dict[str, str]] = []
    key_metrics: List[Dict[str, Any]] = []
    tables: List[Dict[str, Any]] = []
    sections: List[Dict[str, Any]] = []

class ExtractRequest(BaseModel):
    document_id: str
    custom_schema_prompt: Optional[str] = None
    target_type: Optional[str] = None # invoice, contract, resume, generic

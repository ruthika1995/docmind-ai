import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "openrouter" in data
    assert "embeddings" in data
    assert data["embeddings"]["dimension"] == 384

def test_list_documents():
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) >= 4
    filenames = [d["filename"] for d in docs]
    assert any("INV-2026-8842" in f for f in filenames)
    assert any("MSA-2025" in f for f in filenames)

def test_get_document_detail():
    response = client.get("/api/v1/documents/doc-invoice-001")
    assert response.status_code == 200
    doc = response.json()
    assert doc["id"] == "doc-invoice-001"
    assert doc["classification"] == "invoice"
    assert len(doc["chunks"]) > 0

def test_extract_invoice():
    payload = {
        "document_id": "doc-invoice-001",
        "target_type": "invoice"
    }
    response = client.post("/api/v1/extract", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == "doc-invoice-001"
    assert "extracted_data" in data
    assert "line_items" in data["extracted_data"]

def test_compare_contracts():
    payload = {
        "doc_a_id": "doc-contract-v1",
        "doc_b_id": "doc-contract-v2"
    }
    response = client.post("/api/v1/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "diff_summary" in data
    assert "clauses_comparison" in data
    assert len(data["clauses_comparison"]) > 0

def test_rag_chat_with_document():
    payload = {
        "document_id": "doc-invoice-001",
        "message": "What is the total amount due and what is the due date?",
        "stream": False
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "assistant"
    assert len(data["content"]) > 0
    assert len(data["citations"]) > 0

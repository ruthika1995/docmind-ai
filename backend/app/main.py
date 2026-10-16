import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.models.document import Document, DocumentChunk
from app.services.sample_data import SAMPLE_DOCUMENTS
from app.ai.embeddings import embedding_engine
from app.api.v1 import api_router
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

def auto_seed_if_empty():
    db = SessionLocal()
    try:
        count = db.query(Document).count()
        if count == 0:
            logger.info("Initializing database with enterprise sample documents...")
            for s in SAMPLE_DOCUMENTS:
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
            logger.info("Sample documents seeded successfully.")
    except Exception as e:
        logger.warning(f"Auto-seed notice: {e}")
    finally:
        db.close()

# Seed default data
auto_seed_if_empty()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Document Intelligence & RAG Platform powered by OpenRouter Gateway and Decoupled Vector Embeddings."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "service": "DocMind AI Backend",
        "status": "online",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR
    }

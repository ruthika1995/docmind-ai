import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Mount Frontend static files for single-platform fullstack deployment
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/dist"))

if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow /docs and /openapi.json to reach FastAPI
        if full_path in ["docs", "openapi.json", "redoc"]:
            return None
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "service": "DocMind AI Backend",
            "status": "online",
            "docs_url": "/docs",
            "api_v1": settings.API_V1_STR
        }

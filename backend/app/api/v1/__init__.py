from fastapi import APIRouter
from app.api.v1.documents import router as documents_router
from app.api.v1.extract import router as extract_router
from app.api.v1.compare import router as compare_router
from app.api.v1.rag import router as rag_router
from app.api.v1.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(documents_router)
api_router.include_router(extract_router)
api_router.include_router(compare_router)
api_router.include_router(rag_router)

__all__ = ["api_router"]

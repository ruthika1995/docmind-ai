from fastapi import APIRouter
from app.config import settings
from app.ai.openrouter_client import openrouter_client

router = APIRouter(tags=["Health & Gateway"])

@router.get("/health")
def health_check():
    has_api_key = bool(settings.OPENROUTER_API_KEY and "your_key" not in settings.OPENROUTER_API_KEY.lower())
    return {
        "status": "healthy",
        "service": "DocMind AI Gateway",
        "version": settings.VERSION,
        "environment": "development" if not has_api_key else "production",
        "openrouter": {
            "configured": has_api_key,
            "active_model": settings.OPENROUTER_MODEL,
            "gateway_url": settings.OPENROUTER_BASE_URL,
            "fallback_models": openrouter_client.fallback_models,
            "offline_heuristic_available": True
        },
        "embeddings": {
            "engine": "Decoupled Local Dense Embedder",
            "dimension": 384,
            "provider": "Decoupled Architecture"
        }
    }

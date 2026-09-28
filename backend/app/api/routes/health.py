from fastapi import APIRouter
from app.ml.model_loader import model_loader

router = APIRouter()

@router.get("/health")
def health_check():
    """Health check endpoint required by SRS."""
    try:
        pipeline = model_loader.get_pipeline()
        model_loaded = pipeline is not None
    except Exception:
        model_loaded = False

    return {
        "status": "healthy",
        "model_loaded": model_loaded,
        "service": "Q-MedAI"
    }

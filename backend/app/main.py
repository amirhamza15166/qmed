from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import json
import os

from app.core.config import settings
from app.ml.model_loader import model_loader
from app.api.routes import health, prediction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup without catching exceptions (Fail fast if error)
    model_loader.load_pipeline(settings.MODEL_PATH)
    logger.info("Application startup: Model pipeline loaded successfully.")

    # mapping.json loading removed per instructions

    yield
    # Shutdown
    logger.info("Application shutdown.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for the Quantum-Powered Medical Symptom Analyzer",
    version="1.0.0",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(prediction.router, tags=["prediction"])

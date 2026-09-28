from fastapi import HTTPException
import logging
from app.ml.model_loader import model_loader
from app.ml.predictor import Predictor
from app.schemas.prediction import PredictionRequest, PredictionResponse, PredictionResult

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        try:
            pipeline = model_loader.get_pipeline()
            self.predictor = Predictor(pipeline)
        except Exception as e:
            logger.error(f"Prediction service initialization failed: {str(e)}")
            self.predictor = None

    def process_prediction(self, request: PredictionRequest) -> PredictionResponse:
        if self.predictor is None:
            raise HTTPException(status_code=503, detail="Q-MedAI model is currently unavailable.")

        try:
            disease = self.predictor.predict(request.symptoms)
            return PredictionResponse(
                success=True,
                prediction=PredictionResult(
                    disease=disease,
                    confidence=None, # QSVC might not provide calibrated probas
                    model_version="q-medai-v1"
                )
            )
        except Exception as e:
            logger.error(f"Error during prediction service call: {str(e)}")
            raise HTTPException(status_code=500, detail="Unexpected prediction failure.")

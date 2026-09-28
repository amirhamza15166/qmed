from pydantic import BaseModel, Field, constr
from typing import Optional

class PredictionRequest(BaseModel):
    symptoms: constr(min_length=10, max_length=5000) = Field(
        ...,
        description="Natural language description of the patient's symptoms.",
        json_schema_extra={"example": "I have had a severe headache for two days and feel nauseous."}
    )

class PredictionResult(BaseModel):
    disease: str
    confidence: Optional[float] = None
    model_version: str = "q-medai-v1"

class PredictionResponse(BaseModel):
    success: bool
    prediction: str | PredictionResult

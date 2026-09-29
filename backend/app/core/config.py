from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Q-MedAI"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    MODEL_PATH: str = "models/q_medai_pipeline_3.dill"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Force reload for CORS
settings = Settings()

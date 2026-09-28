import dill
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ModelLoader:
    _instance = None
    _pipeline = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    def load_pipeline(self, model_path: str) -> Dict[str, Any]:
        """Loads the Q-MedAI dill artifact directly using standard dill.load."""
        if self._pipeline is not None:
            return self._pipeline

        # Ensure we can find it relative to backend root if it's a relative path
        if not os.path.isabs(model_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            full_path = os.path.join(base_dir, model_path)
        else:
            full_path = model_path

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Model artifact not found at {full_path}")

        logger.info(f"Loading model pipeline from {full_path}...")
        with open(full_path, 'rb') as f:
            pipeline = dill.load(f)
        
        required_keys = ['model', 'tfidf', 'scaler', 'pca', 'angle_scaler']
        missing = [k for k in required_keys if k not in pipeline]
        if missing:
            raise ValueError(f"Pipeline missing required components: {missing}")

        self._pipeline = pipeline
        logger.info("Model pipeline successfully loaded.")
        return self._pipeline

    def get_pipeline(self) -> Dict[str, Any]:
        """Returns the loaded pipeline."""
        if self._pipeline is None:
            raise RuntimeError("Model pipeline has not been loaded. Call load_pipeline first.")
        return self._pipeline

model_loader = ModelLoader()
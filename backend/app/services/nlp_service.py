from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class NLPService:
    def __init__(self):
        logger.info("Initializing Hugging Face models... This may take a moment.")
        try:
            # Flan-T5 for text refinement
            self.refiner = pipeline("text2text-generation", model="google/flan-t5-base")
            # MiniLM for embeddings / feature extraction
            self.embedder = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")
            logger.info("Hugging Face models loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Hugging Face models: {str(e)}")
            self.refiner = None
            self.embedder = None

    def refine_symptoms(self, raw_text: str) -> str:
        """Uses Flan-T5 to convert raw symptoms into clean medical text."""
        if not self.refiner:
            return raw_text
            
        prompt = f"Translate the following raw patient symptoms into a clean, professional medical description: {raw_text}"
        try:
            result = self.refiner(prompt, max_length=128, truncation=True)
            return result[0]['generated_text']
        except Exception as e:
            logger.error(f"Flan-T5 generation failed: {e}")
            return raw_text

    def get_embeddings(self, text: str):
        """Uses MiniLM-L6-v2 to generate semantic vector embeddings."""
        if not self.embedder:
            return []
        try:
            # Returns a nested list of embeddings
            return self.embedder(text)
        except Exception as e:
            logger.error(f"MiniLM embedding generation failed: {e}")
            return []

nlp_service = NLPService()

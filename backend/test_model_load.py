import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.ml.model_loader import model_loader
    
    model_path = Path("models/q_medai_pipeline_3.dill").resolve()
    print(f"Testing load from: {model_path}")
    
    model_loader.load_pipeline(str(model_path))
    pipeline = model_loader.get_pipeline()
    
    if pipeline:
        print("SUCCESS: Model pipeline loaded successfully.")
        print(f"Pipeline type: {type(pipeline)}")
    else:
        print("FAILED: Pipeline is None.")
except Exception as e:
    import traceback
    print("FAILED TO LOAD MODEL:")
    traceback.print_exc()

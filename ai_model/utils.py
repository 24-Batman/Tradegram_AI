import os
from pathlib import Path
from typing import Dict, Any

def load_model_config() -> Dict[str, Any]:
    """Load model configuration settings"""
    return {
        "sentiment_model_path": "ProsusAI/finbert",
        "pattern_model_path": "microsoft/phi-2",  # or another suitable model
        "model_save_dir": str(Path(__file__).parent / "saved_models"),
        "cache_dir": str(Path(__file__).parent / "model_cache")
    } 
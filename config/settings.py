import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Data directories
MARKET_DATA_DIR = ROOT_DIR / "data" / "market_data"
LOGS_DIR = ROOT_DIR / "data" / "logs"

# Ensure directories exist
MARKET_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    API_BASE_URL: str = "https://api.openserv.ai"
    PORT: int = 5500
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    
    # API Keys
    OPENSERV_API_KEY: str
    GEMINI_API_KEY: str
    
    # Trading Parameters
    MIN_TRADE_AMOUNT: float = 0.0001
    MAX_TRADE_AMOUNT: float = 1.0
    DEFAULT_TIMEFRAME: str = "1h"
    
    # Model Settings
    MODEL_CACHE_DIR: str = "ai_model/cache"
    SENTIMENT_MODEL: str = "ProsusAI/finbert"
    PATTERN_MODEL: str = "microsoft/phi-2"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "data/logs/trademateai.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

settings = get_settings() 
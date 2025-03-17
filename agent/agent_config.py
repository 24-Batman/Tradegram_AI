from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AgentConfig:
    """Configuration settings for the TradingAgent"""
    name: str = "TradeMateAI"
    model_type: str = "gemini-2.0-flash"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # API Keys
    openserv_api_key: str = os.getenv("OPENSERV_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    # Trading Parameters
    min_confidence: float = 0.7
    max_position_size: float = 1.0
    stop_loss_percent: float = 0.02
    take_profit_percent: float = 0.05
    
    # Rate Limiting
    max_requests_per_min: int = 60
    request_timeout: int = 30

    def __post_init__(self):
        """Validate configuration after initialization"""
        if not self.openserv_api_key:
            raise ValueError("OPENSERV_API_KEY not found in environment variables")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables") 
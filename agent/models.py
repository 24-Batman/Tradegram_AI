from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

class TradingSignal(Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"

class SentimentType(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

@dataclass
class TradeAnalysis:
    timestamp: datetime
    symbol: str
    recommendation: TradingSignal
    confidence: float
    indicators: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis to dictionary format"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "symbol": self.symbol,
            "recommendation": self.recommendation.value,
            "confidence": self.confidence,
            "indicators": self.indicators
        }

@dataclass
class MarketData:
    symbol: str
    price: float
    volume: float
    change_24h: float
    high_24h: Optional[float] = None
    low_24h: Optional[float] = None
    market_cap: Optional[float] = None

@dataclass
class SentimentAnalysis:
    symbol: str
    sentiment: SentimentType
    confidence: float
    sources: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")

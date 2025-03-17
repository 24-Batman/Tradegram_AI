from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class TradeAnalysis:
    timestamp: datetime
    symbol: str
    recommendation: str
    confidence: float
    indicators: List[str] 
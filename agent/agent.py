import logging
import asyncio
from typing import Dict, Any, Optional
from .agent_config import AgentConfig
from .models import TradeAnalysis
from ai_model.sentiment_analysis import SentimentAnalyzer
from ai_model.trade_analysis import TradeAnalyzer

logger = logging.getLogger(__name__)

class TradingAgent:
    def __init__(self):
        """Initialize the TradingAgent with required components"""
        self.config = AgentConfig()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.trade_analyzer = TradeAnalyzer()
        logger.info(f"Initialized TradingAgent: {self.config.name}")

    async def analyze_market(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Analyze market data for a given symbol"""
        try:
            # Get trade analysis
            pattern_analysis = await self.trade_analyzer.analyze_pattern(symbol)
            if not pattern_analysis:
                raise ValueError(f"No pattern analysis available for {symbol}")

            # Get sentiment analysis
            sentiment_result = await self.sentiment_analyzer.analyze(symbol)
            
            return {
                "symbol": symbol,
                "price": pattern_analysis.get("price", 0.0),
                "change_24h": pattern_analysis.get("change_24h", 0.0),
                "volume": pattern_analysis.get("volume", 0.0),
                "sentiment": sentiment_result.get("sentiment", "neutral"),
                "confidence": sentiment_result.get("confidence", 0.0),
                "recommendation": self._generate_recommendation(pattern_analysis, sentiment_result)
            }
        except Exception as e:
            logger.error(f"Error in market analysis: {str(e)}")
            return None

    async def generate_trade_signal(self, symbol: str) -> Optional[TradeAnalysis]:
        """Generate trading signals based on market analysis"""
        try:
            market_data = await self.analyze_market(symbol)
            if not market_data:
                return None

            return TradeAnalysis(
                timestamp=asyncio.get_event_loop().time(),
                symbol=symbol,
                recommendation=market_data["recommendation"],
                confidence=market_data["confidence"],
                indicators=self._get_active_indicators(market_data)
            )
        except Exception as e:
            logger.error(f"Error generating trade signal: {str(e)}")
            return None

    def _generate_recommendation(self, pattern: Dict[str, Any], sentiment: Dict[str, Any]) -> str:
        """Generate trading recommendation based on technical and sentiment analysis"""
        # Implement your recommendation logic here
        # This is a simplified example
        if pattern.get("trend", "neutral") == "up" and sentiment.get("sentiment") == "positive":
            return "buy"
        elif pattern.get("trend", "neutral") == "down" and sentiment.get("sentiment") == "negative":
            return "sell"
        return "hold"

    def _get_active_indicators(self, market_data: Dict[str, Any]) -> list:
        """Get list of active technical indicators"""
        indicators = []
        if market_data.get("rsi"):
            indicators.append(f"RSI: {market_data['rsi']}")
        if market_data.get("macd"):
            indicators.append(f"MACD: {market_data['macd']}")
        return indicators 
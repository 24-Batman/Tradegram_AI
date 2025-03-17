import logging
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import numpy as np
from .agent_config import AgentConfig
from .models import TradeAnalysis, MarketData, TradingSignal, SentimentAnalysis, SentimentType
from ai_model.sentiment_analysis import SentimentAnalyzer
from ai_model.trade_analysis import TradeAnalyzer
from ai_model.reinforcement import ReinforcementLearner

logger = logging.getLogger(__name__)

class TradingAgent:
    def __init__(self):
        """Initialize the TradingAgent with required components"""
        self.config = AgentConfig()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.trade_analyzer = TradeAnalyzer()
        self.rl_model = ReinforcementLearner()
        logger.info(f"Initialized TradingAgent: {self.config.name}")

    async def analyze_sentiment(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Analyze sentiment for a given symbol"""
        try:
            # Get sentiment analysis from analyzer
            sentiment_result = await self.sentiment_analyzer.analyze(symbol)
            
            if not sentiment_result:
                return None

            # Handle list of sentiment results
            if isinstance(sentiment_result, list):
                if not sentiment_result:  # Empty list check
                    return None
                    
                # Aggregate sentiment results without assuming 'source' key exists
                sentiment_result = {
                    'sentiment': max(s.get("sentiment", "neutral") for s in sentiment_result),
                    'confidence': sum(s.get("confidence", 0.0) for s in sentiment_result) / len(sentiment_result),
                    'sources': list(set(source for s in sentiment_result for source in s.get("sources", [])))
                }

            # Convert to proper format
            return {
                "symbol": symbol,
                "sentiment": sentiment_result.get("sentiment", "neutral"),
                "confidence": sentiment_result.get("confidence", 0.0),
                "sources": sentiment_result.get("sources", []),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return None

    async def analyze_market(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Analyze market data for a given symbol"""
        try:
            # Create a MarketData object with initial data
            market_data = MarketData(
                symbol=symbol,
                price=0.0,  # These will be updated with real data
                volume=0.0,
                change_24h=0.0
            )

            # Get trade analysis
            pattern_analysis = await self.trade_analyzer.analyze_pattern(market_data)
            if not pattern_analysis:
                raise ValueError(f"No pattern analysis available for {symbol}")

            # Get sentiment analysis
            sentiment_result = await self.sentiment_analyzer.analyze(symbol)
            if isinstance(sentiment_result, list):
                sentiment_result = {
                    'sentiment': max(s.get("sentiment", "neutral") for s in sentiment_result),
                    'confidence': sum(s.get("confidence", 0.0) for s in sentiment_result) / len(sentiment_result),
                    'sources': list(set(source for s in sentiment_result for source in s.get("sources", [])))
                }
            
            # Get recommendation
            recommendation = await self._generate_recommendation(pattern_analysis, sentiment_result)
            
            return {
                "symbol": symbol,
                "price": pattern_analysis.get("price", 0.0),
                "change_24h": pattern_analysis.get("change_24h", 0.0),
                "volume": pattern_analysis.get("volume", 0.0),
                "sentiment": sentiment_result.get("sentiment", "neutral"),
                "confidence": sentiment_result.get("confidence", 0.0),
                "recommendation": recommendation.value.upper()  # Ensure uppercase string
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

            # Convert string recommendation to TradingSignal enum
            recommendation_str = market_data["recommendation"].upper()
            recommendation = TradingSignal[recommendation_str]

            return TradeAnalysis(
                timestamp=datetime.now(timezone.utc),
                symbol=symbol,
                recommendation=recommendation,  # Now passing TradingSignal enum
                confidence=market_data["confidence"],
                indicators=self._get_active_indicators(market_data)
            )
        except Exception as e:
            logger.error(f"Error generating trade signal: {str(e)}")
            return None

    def _prepare_state(self, pattern_analysis: Dict[str, Any], sentiment_result: Dict[str, Any]) -> np.ndarray:
        """Prepare state vector for reinforcement learning model"""
        state = np.zeros(10)  # Match the state_size in ReinforcementLearner
        
        # Technical indicators (0-4)
        state[0] = float(pattern_analysis.get("rsi", 50.0)) / 100.0  # Normalize RSI
        state[1] = float(pattern_analysis.get("macd", {}).get("value", 0.0))
        state[2] = float(pattern_analysis.get("volume", 0.0)) / 1e6  # Normalize volume
        state[3] = float(pattern_analysis.get("change_24h", 0.0)) / 100.0  # Normalize price change
        
        # Convert trend to numeric value
        trend_map = {"up": 1.0, "down": -1.0, "neutral": 0.0}
        trend = pattern_analysis.get("trend", "neutral")
        state[4] = trend_map.get(trend, 0.0)

        # Sentiment features (5-9)
        # Convert sentiment to numeric values
        sentiment = sentiment_result.get("sentiment", SentimentType.NEUTRAL)
        # Handle both string and enum sentiment values
        if isinstance(sentiment, str):
            sentiment = sentiment.lower()
        elif isinstance(sentiment, SentimentType):
            sentiment = sentiment.value

        sentiment_map = {
            "positive": 1.0,
            SentimentType.POSITIVE.value: 1.0,
            "negative": -1.0,
            SentimentType.NEGATIVE.value: -1.0,
            "neutral": 0.0,
            SentimentType.NEUTRAL.value: 0.0
        }
        state[5] = sentiment_map.get(sentiment, 0.0)  # Sentiment value
        state[6] = float(sentiment_result.get("confidence", 0.0))  # Sentiment confidence
        
        # Market volatility and volume metrics
        state[7] = float(pattern_analysis.get("volatility", 0.0))
        state[8] = float(pattern_analysis.get("volume_change", 0.0)) / 100.0
        state[9] = float(len(sentiment_result.get("sources", []))) / 10.0  # Normalize source count

        return state

    async def _generate_recommendation(self, pattern_analysis: Dict[str, Any], sentiment_result: Dict[str, Any]) -> TradingSignal:
        """Generate trading recommendation using reinforcement learning model"""
        try:
            # Prepare state vector
            state = self._prepare_state(pattern_analysis, sentiment_result)
            
            # Get action from RL model
            action = await self.rl_model.predict_action(state)
            
            # Convert action to TradingSignal
            signal_map = {
                0: TradingSignal.BUY,
                1: TradingSignal.SELL,
                2: TradingSignal.HOLD
            }
            
            # Use traditional logic as fallback
            if action not in signal_map:
                return await self._traditional_recommendation(pattern_analysis, sentiment_result)
                
            return signal_map[action]
            
        except Exception as e:
            logger.error(f"Error in RL recommendation: {str(e)}")
            # Fallback to traditional recommendation
            return await self._traditional_recommendation(pattern_analysis, sentiment_result)

    async def _traditional_recommendation(self, pattern_analysis: Dict[str, Any], sentiment_result: Dict[str, Any]) -> TradingSignal:
        """Traditional rule-based recommendation as fallback"""
        sentiment = sentiment_result.get("sentiment", "neutral")
        confidence = sentiment_result.get("confidence", 0.0)

        if confidence > 0.75 and sentiment == "positive":
            if pattern_analysis.get("rsi", 50) < 30:
                return TradingSignal.BUY
            if pattern_analysis.get("macd", {}).get("value", 0) > 0:
                return TradingSignal.BUY

        elif confidence > 0.75 and sentiment == "negative":
            if pattern_analysis.get("rsi", 50) > 70:
                return TradingSignal.SELL
            if pattern_analysis.get("macd", {}).get("value", 0) < 0:
                return TradingSignal.SELL

        return TradingSignal.HOLD

    def _get_active_indicators(self, market_data: Dict[str, Any]) -> list:
        """Get list of active technical indicators"""
        indicators = []
        if market_data.get("rsi"):
            indicators.append(f"RSI: {market_data['rsi']}")
        if market_data.get("macd"):
            indicators.append(f"MACD: {market_data['macd']}")
        return indicators if indicators else ['No significant indicators']
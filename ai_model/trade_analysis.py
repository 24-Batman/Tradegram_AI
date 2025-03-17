import logging
import numpy as np
from typing import Dict, Any, Optional, List
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
from agent.models import MarketData, TradingSignal

logger = logging.getLogger(__name__)

class TradeAnalyzer:
    def __init__(self):
        """Initialize trade analysis components"""
        self.patterns = []
        self.scaler = MinMaxScaler()
        self._initialize_indicators()
        
    def _initialize_indicators(self):
        """Initialize technical indicators"""
        self.indicators = {
            'RSI': self._calculate_rsi,
            'MACD': self._calculate_macd,
            'BB': self._calculate_bollinger_bands
        }

    async def analyze_pattern(self, market_data: MarketData) -> Dict[str, Any]:
        """Analyze trading patterns from market data"""
        try:
            # Convert market data to DataFrame for analysis
            df = self._prepare_data(market_data)
            
            # Calculate technical indicators
            indicators = self._calculate_indicators(df)
            
            # Analyze patterns
            patterns = self._detect_patterns(df, indicators)
            
            # Generate trading signals
            signals = await self.generate_signals(patterns)
            
            return {
                'price': market_data.price,
                'change_24h': market_data.change_24h,
                'volume': market_data.volume,
                'indicators': indicators,
                'patterns': patterns,
                'signals': signals,
                'trend': self._determine_trend(patterns)
            }

        except Exception as e:
            logger.error(f"Error in pattern analysis: {str(e)}")
            return None

    async def generate_signals(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trading signals based on pattern analysis"""
        try:
            # Combine different pattern signals
            signal_strength = self._calculate_signal_strength(patterns)
            
            return {
                'signal': self._determine_signal(signal_strength),
                'strength': signal_strength,
                'confidence': self._calculate_confidence(patterns)
            }
        except Exception as e:
            logger.error(f"Error generating signals: {str(e)}")
            return None

    def _prepare_data(self, market_data: MarketData) -> pd.DataFrame:
        """Prepare market data for analysis"""
        data = {
            'price': [market_data.price],
            'volume': [market_data.volume],
            'change_24h': [market_data.change_24h]
        }
        return pd.DataFrame(data)

    def _calculate_indicators(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate technical indicators"""
        results = {}
        for name, func in self.indicators.items():
            try:
                results[name] = func(df)
            except Exception as e:
                logger.error(f"Error calculating {name}: {str(e)}")
                results[name] = None
        return results

    def _calculate_rsi(self, df: pd.DataFrame, periods: int = 14) -> float:
        """Calculate Relative Strength Index"""
        try:
            # Calculate price changes
            delta = df['price'].diff()
            
            # Separate gains and losses
            gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
            
            # Calculate RS and RSI
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi.iloc[-1]
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return 50.0

    def _calculate_macd(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate MACD indicator"""
        try:
            # Calculate EMAs
            exp1 = df['price'].ewm(span=12, adjust=False).mean()
            exp2 = df['price'].ewm(span=26, adjust=False).mean()
            
            # Calculate MACD line and signal line
            macd_line = exp1 - exp2
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            
            # Calculate histogram
            histogram = macd_line - signal_line
            
            return {
                'macd': macd_line.iloc[-1],
                'signal': signal_line.iloc[-1],
                'hist': histogram.iloc[-1]
            }
        except Exception as e:
            logger.error(f"Error calculating MACD: {str(e)}")
            return {'macd': 0.0, 'signal': 0.0, 'hist': 0.0}

    def _calculate_bollinger_bands(self, df: pd.DataFrame, window: int = 20) -> Dict[str, float]:
        """Calculate Bollinger Bands"""
        try:
            # Calculate middle band (20-day SMA)
            middle_band = df['price'].rolling(window=window).mean()
            
            # Calculate standard deviation
            std_dev = df['price'].rolling(window=window).std()
            
            # Calculate upper and lower bands
            upper_band = middle_band + (std_dev * 2)
            lower_band = middle_band - (std_dev * 2)
            
            return {
                'upper': upper_band.iloc[-1],
                'middle': middle_band.iloc[-1],
                'lower': lower_band.iloc[-1]
            }
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {str(e)}")
            return {'upper': 0.0, 'middle': 0.0, 'lower': 0.0}

    def _detect_patterns(self, df: pd.DataFrame, indicators: Dict[str, Any]) -> List[str]:
        """Detect chart patterns"""
        patterns = []
        try:
            price = df['price'].iloc[-1]
            
            # Check for oversold/overbought conditions
            if indicators['RSI'] < 30:
                patterns.append('oversold')
            elif indicators['RSI'] > 70:
                patterns.append('overbought')
            
            # Check for MACD crossovers
            if indicators['MACD']['hist'] > 0 and indicators['MACD']['macd'] > indicators['MACD']['signal']:
                patterns.append('bullish_crossover')
            elif indicators['MACD']['hist'] < 0 and indicators['MACD']['macd'] < indicators['MACD']['signal']:
                patterns.append('bearish_crossover')
            
            # Check Bollinger Band signals
            bb = indicators['BB']
            if price > bb['upper']:
                patterns.append('bb_upper_break')
            elif price < bb['lower']:
                patterns.append('bb_lower_break')
            
            return patterns
        except Exception as e:
            logger.error(f"Error detecting patterns: {str(e)}")
            return patterns

    def _determine_trend(self, patterns: List[str]) -> str:
        """Determine overall trend from patterns"""
        try:
            bullish_patterns = ['oversold', 'bullish_crossover', 'bb_lower_break']
            bearish_patterns = ['overbought', 'bearish_crossover', 'bb_upper_break']
            
            bullish_count = sum(1 for p in patterns if p in bullish_patterns)
            bearish_count = sum(1 for p in patterns if p in bearish_patterns)
            
            if bullish_count > bearish_count:
                return "up"
            elif bearish_count > bullish_count:
                return "down"
            return "neutral"
        except Exception as e:
            logger.error(f"Error determining trend: {str(e)}")
            return "neutral"

    def _calculate_signal_strength(self, patterns: Dict[str, Any]) -> float:
        """Calculate signal strength based on patterns"""
        try:
            # Base strength on number and type of confirming patterns
            strength = 0.5  # Start at neutral
            
            # Add strength for trend-confirming patterns
            trend = patterns.get('trend', 'neutral')
            confirming_patterns = sum(1 for p in patterns.get('patterns', [])
                                   if (trend == 'up' and p in ['bullish_crossover', 'oversold']) or
                                      (trend == 'down' and p in ['bearish_crossover', 'overbought']))
            
            # Adjust strength based on confirming patterns
            strength += (confirming_patterns * 0.1)  # Each confirming pattern adds 0.1
            
            # Normalize to [0, 1]
            return max(0.0, min(1.0, strength))
        except Exception as e:
            logger.error(f"Error calculating signal strength: {str(e)}")
            return 0.5

    def _determine_signal(self, strength: float) -> TradingSignal:
        """Determine trading signal based on strength"""
        if strength > 0.7:
            return TradingSignal.BUY
        elif strength < 0.3:
            return TradingSignal.SELL
        return TradingSignal.HOLD

    def _calculate_confidence(self, patterns: Dict[str, Any]) -> float:
        """Calculate confidence level of the analysis"""
        try:
            # Base confidence calculation
            confidence = 0.5
            
            # Add confidence based on number of confirming signals
            pattern_count = len(patterns.get('patterns', []))
            confidence += (pattern_count * 0.1)  # Each pattern adds 0.1 confidence
            
            # Adjust confidence based on indicator agreement
            if patterns.get('trend') != 'neutral':
                confidence += 0.2  # Clear trend adds confidence
            
            # Normalize to [0, 1]
            return max(0.0, min(1.0, confidence))
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 0.8 
import logging
import numpy as np
from typing import Dict, Any, Optional
import torch
from transformers import pipeline
from .model import TradingModel
from agent.models import SentimentType

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analysis components"""
        self.model = None
        self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the sentiment analysis pipeline"""
        try:
            # Using FinBERT for financial sentiment analysis
            self.model = pipeline(
                "sentiment-analysis",
                model="ProsusAI/finbert",
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info("Sentiment analysis model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing sentiment model: {str(e)}")
            raise

    async def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of market-related text"""
        try:
            # Perform sentiment analysis
            result = self.model(text)[0]
            sentiment_label = result['label']
            confidence = result['score']

            # Map sentiment labels to SentimentType
            sentiment_mapping = {
                'positive': SentimentType.POSITIVE,
                'negative': SentimentType.NEGATIVE,
                'neutral': SentimentType.NEUTRAL
            }

            return {
                'sentiment': sentiment_mapping.get(sentiment_label.lower(), SentimentType.NEUTRAL),
                'confidence': confidence,
                'sources': ['FinBERT Analysis'],
                'raw_score': self._normalize_sentiment_score(confidence, sentiment_label)
            }

        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return {
                'sentiment': SentimentType.NEUTRAL,
                'confidence': 0.0,
                'sources': [],
                'raw_score': 0.0
            }

    def _normalize_sentiment_score(self, confidence: float, label: str) -> float:
        """Normalize sentiment score to range [-1, 1]"""
        if label.lower() == 'negative':
            return -confidence
        elif label.lower() == 'positive':
            return confidence
        return 0.0 
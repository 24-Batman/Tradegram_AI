import logging
import torch
from typing import Dict, Any, List
from transformers import pipeline
from agent.models import SentimentType

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analysis components"""
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    async def initialize(self):
        """Load the FinBERT model asynchronously"""
        try:
            self.model = pipeline(
                "sentiment-analysis",
                model="ProsusAI/finbert",
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info("Sentiment analysis model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing sentiment model: {str(e)}")
            raise

    async def analyze(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analyze sentiment of a list of texts"""
        try:
            if not self.model:
                await self.initialize()

            # Ensure input is a list (single string wrapped in a list)
            if isinstance(texts, str):
                texts = [texts]

            # Process in chunks if text is too long
            results = self.model(texts)

            # Convert results into structured response
            sentiment_mapping = {
                'positive': SentimentType.POSITIVE,
                'negative': SentimentType.NEGATIVE,
                'neutral': SentimentType.NEUTRAL
            }

            return [
                {
                    'text': text,
                    'sentiment': sentiment_mapping.get(res['label'].lower(), SentimentType.NEUTRAL),
                    'confidence': res['score'],
                    'sources': ['FinBERT Analysis'],
                    'raw_score': self._normalize_sentiment_score(res['score'], res['label'])
                }
                for text, res in zip(texts, results)
            ]

        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return [
                {
                    'text': text,
                    'sentiment': SentimentType.NEUTRAL,
                    'confidence': 0.0,
                    'sources': [],
                    'raw_score': 0.0
                }
                for text in texts
            ]

    def _normalize_sentiment_score(self, confidence: float, label: str) -> float:
        """Normalize sentiment score to range [-1, 1]"""
        if label.lower() == 'negative':
            return -confidence
        elif label.lower() == 'positive':
            return confidence
        return 0.0

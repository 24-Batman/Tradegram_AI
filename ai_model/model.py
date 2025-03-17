import logging
import torch
from pathlib import Path
from typing import Dict, Any, Optional
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoModelForCausalLM
from .utils import load_model_config

logger = logging.getLogger(__name__)

class TradingModel:
    def __init__(self):
        """Initialize AI models for trading analysis"""
        self.model_name = "trading_model_v1"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load model configurations
        self.config = load_model_config()
        
        # Initialize models
        self._init_sentiment_model()
        self._init_pattern_model()
        logger.info(f"TradingModel initialized on device: {self.device}")

    def _init_sentiment_model(self):
        """Initialize the sentiment analysis model"""
        try:
            model_path = self.config["sentiment_model_path"]
            self.sentiment_tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(model_path)
            self.sentiment_model.to(self.device)
            self.sentiment_model.eval()
        except Exception as e:
            logger.error(f"Error loading sentiment model: {str(e)}")
            raise

    def _init_pattern_model(self):
        """Initialize the pattern recognition model"""
        try:
            model_path = self.config["pattern_model_path"]
            self.pattern_tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.pattern_model = AutoModelForCausalLM.from_pretrained(model_path)
            self.pattern_model.to(self.device)
            self.pattern_model.eval()
        except Exception as e:
            logger.error(f"Error loading pattern model: {str(e)}")
            raise

    async def predict(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make predictions using both sentiment and pattern analysis"""
        try:
            sentiment_score = await self._analyze_sentiment(data.get("text", ""))
            pattern_score = await self._analyze_pattern(data.get("market_data", {}))
            
            return {
                "sentiment": sentiment_score,
                "pattern": pattern_score,
                "combined_score": self._combine_scores(sentiment_score, pattern_score)
            }
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return None

    async def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of market-related text"""
        with torch.no_grad():
            inputs = self.sentiment_tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(self.device)
            
            outputs = self.sentiment_model(**inputs)
            scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
            return scores[0][1].item()  # Return positive sentiment score

    async def _analyze_pattern(self, market_data: Dict[str, Any]) -> Dict[str, float]:
        """Analyze market patterns for trading signals"""
        # Convert market data to model input format
        pattern_input = self._prepare_pattern_input(market_data)
        
        with torch.no_grad():
            outputs = self.pattern_model(**pattern_input)
            # Process model outputs for pattern recognition
            return self._process_pattern_outputs(outputs)

    def _prepare_pattern_input(self, market_data: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        """Prepare market data for pattern analysis"""
        try:
            # Extract relevant features
            features = [
                market_data.get('price', 0.0),
                market_data.get('volume', 0.0),
                market_data.get('change_24h', 0.0),
                market_data.get('rsi', 50.0),
                market_data.get('macd', 0.0)
            ]
            
            # Convert to tensor
            tensor_input = torch.tensor(features, dtype=torch.float32).unsqueeze(0).to(self.device)
            
            return {
                'input_ids': tensor_input,
                'attention_mask': torch.ones_like(tensor_input)
            }
        except Exception as e:
            logger.error(f"Error preparing pattern input: {str(e)}")
            raise

    def _process_pattern_outputs(self, outputs) -> Dict[str, float]:
        """Process model outputs into trading signals"""
        try:
            # Get raw predictions
            logits = outputs.logits[0]
            probabilities = torch.softmax(logits, dim=-1)
            
            # Convert to trading signals
            signals = {
                'buy_probability': probabilities[0].item(),
                'sell_probability': probabilities[1].item(),
                'hold_probability': probabilities[2].item(),
                'trend_strength': torch.max(probabilities).item()
            }
            
            return signals
        except Exception as e:
            logger.error(f"Error processing pattern outputs: {str(e)}")
            raise

    def _combine_scores(self, sentiment_score: float, pattern_score: Dict[str, float]) -> float:
        """Combine sentiment and pattern scores for final prediction"""
        try:
            # Weight factors for different components
            sentiment_weight = 0.3
            pattern_weight = 0.7
            
            # Calculate pattern score
            pattern_value = (
                pattern_score['buy_probability'] -
                pattern_score['sell_probability']
            ) * pattern_score['trend_strength']
            
            # Combine scores
            combined_score = (
                sentiment_weight * sentiment_score +
                pattern_weight * pattern_value
            )
            
            # Normalize to [-1, 1]
            return max(min(combined_score, 1.0), -1.0)
        except Exception as e:
            logger.error(f"Error combining scores: {str(e)}")
            return 0.0

    async def train(self, training_data: Dict[str, Any]):
        """Train or fine-tune the models with new data"""
        # Implement training logic
        pass

    def save_models(self, path: str):
        """Save models to disk"""
        save_path = Path(path)
        save_path.mkdir(parents=True, exist_ok=True)
        
        self.sentiment_model.save_pretrained(save_path / "sentiment")
        self.pattern_model.save_pretrained(save_path / "pattern")
        logger.info(f"Models saved to {save_path}") 
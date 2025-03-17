from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from agent.agent import TradingAgent
from agent.models import TradeAnalysis, MarketData, SentimentAnalysis

router = APIRouter()
trading_agent = TradingAgent()

class MarketAnalysisRequest(BaseModel):
    symbol: str = Field(..., description="Trading pair symbol (e.g., BTC/USD)")
    timeframe: str = Field("1h", description="Analysis timeframe")
    include_sentiment: bool = Field(True, description="Include sentiment analysis")

class TradeSignalRequest(BaseModel):
    symbol: str
    amount: float = Field(..., gt=0)
    side: str = Field(..., pattern="^(buy|sell)$")

@router.post("/analyze/market", response_model=Dict[str, Any])
async def analyze_market(request: MarketAnalysisRequest):
    """Analyze market conditions for a given symbol"""
    try:
        analysis = await trading_agent.analyze_market(request.symbol)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not available")
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/sentiment")
async def analyze_sentiment(symbol: str):
    """Analyze market sentiment for a given symbol"""
    try:
        sentiment = await trading_agent.sentiment_analyzer.analyze(symbol)
        if not sentiment:
            raise HTTPException(status_code=404, detail="Sentiment analysis not available")
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/signal/generate")
async def generate_signal(request: TradeSignalRequest):
    """Generate trading signals based on analysis"""
    try:
        signal = await trading_agent.generate_trade_signal(request.symbol)
        if not signal:
            raise HTTPException(status_code=404, detail="No trading signal available")
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market/data/{symbol}")
async def get_market_data(symbol: str):
    """Get current market data for a symbol"""
    try:
        market_data = await trading_agent.get_market_data(symbol)
        if not market_data:
            raise HTTPException(status_code=404, detail="Market data not available")
        return market_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
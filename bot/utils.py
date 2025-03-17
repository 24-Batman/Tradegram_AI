import logging
import aiohttp
from datetime import datetime
from typing import Dict, Any, Optional
from config.settings import settings
from data.logs.logger import setup_logger

logger = setup_logger(__name__)


def setup_logging():
    """Configure logging settings"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=settings.LOG_LEVEL,
        handlers=[
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def format_kraken_symbol(symbol: str) -> str:
    """Convert common symbol format to Kraken format"""
    # Remove '/' if present and convert to uppercase
    clean_symbol = symbol.replace('/', '').upper()
    # Map common names to Kraken pairs if needed
    symbol_map = {
        'BTCUSD': 'XBTUSD',
        'BTCEUR': 'XBTEUR',
        'ETHUSD': 'XETHUSD',
        'ETHEUR': 'XETHZEUR',
        'XRPUSD': 'XXRPUSD',
        'XRPETH': 'XXRPETH',
        'XRPUSD': 'XXRPUSD',
        'XRPETH': 'XXRPETH',
        'SOLUSD': 'SOLUSD',
        'SOLUSDT': 'SOLUSDT',
        'SOLBTC': 'SOLBTC',
        'SOLXRP': 'SOLXRP',
        'SOLETH': 'SOLETH',
        'SOLJPY': 'SOLJPY',
        'SOLXRP': 'SOLXRP',
        'SOLETH': 'SOLETH',
        'SOLJPY': 'SOLJPY',
    }
    return symbol_map.get(clean_symbol, clean_symbol)

async def fetch_market_data(symbol: str) -> Optional[Dict[str, Any]]:
    """Fetch real-time market data from Kraken"""
    try:
        kraken_symbol = format_kraken_symbol(symbol)
        url = f"{settings.API_BASE_URL_KRAKEN}/public/Ticker?pair={kraken_symbol}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=settings.REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("error"):
                        logger.error(f"Kraken API error: {data['error']}")
                        return None
                        
                    result = data.get("result", {})
                    if not result:
                        logger.error("No data in Kraken response")
                        return None
                        
                    # Get the first (and usually only) ticker data
                    ticker_data = next(iter(result.values()))
                    
                    return {
                        "symbol": symbol,
                        "price": float(ticker_data["c"][0]),  # Current price
                        "change_24h": float(ticker_data["p"][1]),  # 24h price change
                        "volume": float(ticker_data["v"][1]),  # 24h volume
                        "high": float(ticker_data["h"][1]),  # 24h high
                        "low": float(ticker_data["l"][1]),  # 24h low
                        "timestamp": datetime.now().timestamp()
                    }
                else:
                    logger.error(f"Kraken API error: Status {response.status}")
                    return None
                    
    except Exception as e:
        logger.error(f"Error fetching market data from Kraken: {str(e)}")
        return None

def format_price_data(data: Dict[str, Any]) -> str:
    """Format market data for display"""
    try:
        if not data:
            return "❌ No market data available"
            
        return (
            f"📊 {data['symbol']} Market Data\n\n"
            f"💰 Price: ${data['price']:,.2f}\n"
            f"📈 24h Change: {data['change_24h']:+.2f}%\n"
            f"📊 Volume: ${data['volume']:,.0f}\n"
            f"📈 24h High: ${data['high']:,.2f}\n"
            f"📉 24h Low: ${data['low']:,.2f}\n"
            f"🕒 Updated: {datetime.fromtimestamp(data['timestamp']).strftime('%H:%M:%S')}"
        )
    except Exception as e:
        logger.error(f"Error formatting price data: {str(e)}")
        return "❌ Error formatting market data"

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') 
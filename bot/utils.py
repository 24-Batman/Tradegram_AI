import logging
import aiohttp
from datetime import datetime
from typing import Dict, Any
from config import API_BASE_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

def setup_logging():
    """Configure logging settings"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("data/logs/bot.log"),
            logging.StreamHandler()
        ]
    )

def format_price_data(data: Dict[str, Any]) -> str:
    """Format price data for user display"""
    return (
        f"💰 {data['symbol']} Price Analysis\n\n"
        f"Current Price: ${data['price']:,.2f}\n"
        f"24h Change: {data['change_24h']:+.2f}%\n"
        f"Volume: ${data['volume']:,.2f}\n"
        f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

async def fetch_market_data(symbol: str) -> Dict[str, Any]:
    """Fetch market data from API"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{API_BASE_URL}/market/{symbol}",
                timeout=REQUEST_TIMEOUT
            ) as response:
                if response.status == 200:
                    return await response.json()
                raise Exception(f"API returned status {response.status}")
        except Exception as e:
            logger.error(f"Error fetching market data: {str(e)}")
            raise

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') 
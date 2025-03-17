import logging
import aiohttp
from typing import Dict, Any, Optional
from config import settings
from datetime import datetime

logger = logging.getLogger(__name__)

class RequestHandler:
    def __init__(self):
        """Initialize request handler with configuration"""
        self.base_url = settings.API_BASE_URL
        self.timeout = settings.REQUEST_TIMEOUT
        self.max_retries = settings.MAX_RETRIES

    async def process_request(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process API request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/{endpoint}",
                        json=data,
                        timeout=self.timeout
                    ) as response:
                        if response.status == 200:
                            return await response.json()
                        
                        logger.error(
                            f"Request failed (attempt {attempt + 1}/{self.max_retries}): "
                            f"Status {response.status}"
                        )
                        
            except Exception as e:
                logger.error(f"Request error (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                
            if attempt < self.max_retries - 1:
                await self._wait_before_retry(attempt)
                
        return None

    async def _wait_before_retry(self, attempt: int):
        """Implement exponential backoff for retries"""
        import asyncio
        wait_time = min(2 ** attempt, 30)  # Max 30 seconds
        await asyncio.sleep(wait_time)

    def validate_request(self, data: Dict[str, Any]) -> bool:
        """Validate request data"""
        required_fields = ['symbol', 'timeframe']
        return all(field in data for field in required_fields)

    async def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle and format error responses"""
        logger.error(f"Error processing request: {str(error)}")
        return {
            "status": "error",
            "message": str(error),
            "timestamp": datetime.utcnow().isoformat()
        } 
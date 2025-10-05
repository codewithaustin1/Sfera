import aiohttp
import logging
from typing import List, Dict, Any
from core.schemas.response import ValidatorRequest, ValidatorResponseItem

class ValidatorClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    async def validate_queries(self, queries: List[str]) -> List[ValidatorResponseItem]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/v1/validate",
                    json={"query": queries}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [ValidatorResponseItem(**item) for item in data]
                    else:
                        logging.error(f"Validator API error: {response.status}")
                        return []
        except Exception as e:
            logging.error(f"Validator client error: {e}")
            return []
import aiohttp
import logging
import re
from typing import List, Dict, Any
from core.schemas.response import ValidatorResponseItem, ValidatorRequest


class ValidatorClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def _fallback_validation(self, queries: List[str]) -> List[ValidatorResponseItem]:
        """Fallback validation when Validator IS is unavailable"""
        results = []
        
        for query in queries:
            # Simple regex patterns for common data types
            phone_pattern = r'^7\d{10}$'  # Russian phone format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if re.match(phone_pattern, query):
                data_type = "phone"
            elif re.match(email_pattern, query):
                data_type = "email"
            else:
                data_type = "unknown"
            
            # Create response item with proper structure
            result_item = {
                "headers": {"sender": "tw.tools.validator"},
                "body": {
                    "request_data": query,
                    "type": data_type,
                    "clean_data": query
                },
                "extra": {"fallback": True}
            }
            
            # Convert to ValidatorResponseItem
            results.append(ValidatorResponseItem(**result_item))
        
        return results
    
    async def validate_queries(self, queries: List[str]) -> List[ValidatorResponseItem]:
        """
        Validate queries using SMK-RK Validator IS with fallback
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/v1/validate",
                    json={"query": queries},
                    timeout=10
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Convert each item to ValidatorResponseItem
                        return [ValidatorResponseItem(**item) for item in data]
                    else:
                        logging.error(f"Validator API returned status: {response.status}")
                        # Use fallback validation
                        return self._fallback_validation(queries)
        except Exception as e:
            logging.error(f"Validator client error: {e}")
            # Use fallback validation when API is unavailable
            return self._fallback_validation(queries)
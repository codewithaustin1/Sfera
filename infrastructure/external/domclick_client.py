import aiohttp
import logging
from typing import Dict, Any

class DomClickClient:
    def __init__(self):
        self.base_url = "https://api.domclick.ru"
        self.headers = {
            "Accept": "application/json",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "x-User-Context": "CUSTOMER",
            "x-User-Role": "CUSTOMER"
        }
    
    async def search_user(self, phone: str) -> Dict[str, Any]:
        params = {
            "phone": phone[1:],  # Remove country code prefix
            "personTypeId": "21020"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/portal/api/v1/user_info",
                params=params,
                headers=self.headers,
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    raise Exception("Unauthorized access to DomClick API")
                else:
                    response.raise_for_status()
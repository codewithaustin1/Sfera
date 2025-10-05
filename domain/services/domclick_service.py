import logging
from typing import Optional
from domain.interfaces.search_service import ISearchService
from domain.models.search import SearchResult
from infrastructure.external.domclick_client import DomClickClient

class DomClickService(ISearchService):
    def __init__(self):
        self.client = DomClickClient()
    
    async def search(self, phone: str) -> list[SearchResult]:
        try:
            response = await self.client.search_user(phone)
            return self._adapt_response(response)
        except Exception as e:
            logging.error(f"Search failed for {phone}: {e}")
            return []
    
    def _adapt_response(self, response: dict) -> list[SearchResult]:
        cas_id = response.get("casId")
        if not cas_id:
            return []
            
        return [SearchResult(
            first_name=response.get("firstName"),
            middle_name=response.get("middleName"),
            last_name=response.get("lastName"),
            user_id=int(cas_id),
            is_registered="Да" if cas_id else "Нет",
            is_partner="Да" if response.get("partnerCard") else "Нет",
            avatar=response.get("partnerCard", {}).get("photoUrl"),
            partner_link=f"https://agencies.domclick.ru/agent/{cas_id}" if response.get("partnerCard") else None,
            client_review=response.get("partnerCard", {}).get("clientReview"),
            registered_at=response.get("partnerCard", {}).get("registeredAt"),
            deals_count=response.get("partnerCard", {}).get("dealsCount"),
            client_comments_count=response.get("partnerCard", {}).get("clientCommentsCount")
        )]
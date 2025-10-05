import logging
from typing import List
from domain.interfaces.search_service import ISearchService
from domain.models.search import SearchResult
from infrastructure.external.domclick_client import DomClickClient

class DomClickService(ISearchService):
    def __init__(self):
        self.client = DomClickClient()
    
    async def search(self, phone: str) -> List[SearchResult]:
        try:
            response = await self.client.search_user(phone)
            return self._adapt_response(response)
        except Exception as e:
            logging.error(f"DomClick search failed for {phone}: {e}")
            return []
    
    def _adapt_response(self, response: dict) -> List[SearchResult]:
        cas_id = response.get("casId")
        if not cas_id:
            return []
            
        first_name = response.get("firstName")
        middle_name = response.get("middleName") 
        last_name = response.get("lastName")
        partner_card = response.get("partnerCard", {})
        
        return [SearchResult(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            user_id=int(cas_id),
            is_registered="Да" if cas_id else "Нет",
            is_partner="Да" if partner_card else "Нет",
            avatar=partner_card.get("photoUrl"),
            partner_link=f"https://agencies.domclick.ru/agent/{cas_id}" if partner_card else None,
            client_review=partner_card.get("clientReview"),
            registered_at=partner_card.get("registeredAt"),
            deals_count=partner_card.get("dealsCount"),
            client_comments_count=partner_card.get("clientCommentsCount")
        )]
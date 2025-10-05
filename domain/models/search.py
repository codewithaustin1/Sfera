from pydantic import BaseModel
from typing import Optional

class SearchResult(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str] 
    last_name: Optional[str]
    user_id: Optional[int]
    is_registered: str
    is_partner: str
    avatar: Optional[str]
    partner_link: Optional[str]
    client_review: Optional[str]
    registered_at: Optional[str]
    deals_count: Optional[int]
    client_comments_count: Optional[int]
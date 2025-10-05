from pydantic import BaseModel
from typing import Optional

class SearchResult(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    is_registered: str = "Нет"
    is_partner: str = "Нет"
    avatar: Optional[str] = None
    partner_link: Optional[str] = None
    client_review: Optional[str] = None
    registered_at: Optional[str] = None
    deals_count: Optional[int] = None
    client_comments_count: Optional[int] = None
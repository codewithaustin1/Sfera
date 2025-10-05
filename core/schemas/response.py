from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class StandardResponse(BaseModel):
    headers: Dict[str, str]
    body: Dict[str, Any]
    extra: Optional[Dict[str, Any]] = None

class ValidatorRequest(BaseModel):
    query: List[str]

class ValidatorResponseItem(BaseModel):
    headers: Dict[str, str]
    body: Dict[str, Any]
    extra: Optional[Dict[str, Any]] = None
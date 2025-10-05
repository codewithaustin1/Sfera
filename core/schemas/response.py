from pydantic import BaseModel
from typing import Any, Dict, Optional

class StandardResponse(BaseModel):
    headers: Dict[str, str]
    body: Dict[str, Any]
    extra: Optional[Dict[str, Any]] = None
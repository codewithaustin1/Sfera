from fastapi import APIRouter, HTTPException
from domain.services.domclick_service import DomClickService
from core.schemas.response import StandardResponse

router = APIRouter()
search_service = DomClickService()

@router.get("/search/phone/{phone}", response_model=StandardResponse)
async def search_phone(phone: str):
    try:
        results = await search_service.search(phone)
        return StandardResponse(
            headers={"sender": "domclick-service"},
            body={"results": [result.dict() for result in results]},
            extra={"query": phone, "results_count": len(results)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
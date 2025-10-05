from fastapi import APIRouter, HTTPException
import aiohttp
from typing import List
from core.schemas.response import StandardResponse
from core.config import settings

router = APIRouter()

@router.post("/process", response_model=List[StandardResponse])
async def process_queries(queries: List[str]):
    results = []
    
    for query in queries:
        # Validate query type using Validator IS
        data_type = await _get_data_type(query)
        
        # Route to appropriate service based on data type
        if data_type == "phone":
            result = await _call_phone_service(query)
            results.append(result)

        
    return results

async def _get_data_type(query: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.VALIDATOR_ENDPOINT}/api/v1/validate",
            json={"query": [query]}
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data[0]["body"]["type"] if data else "unknown"
    return "unknown"

async def _call_phone_service(phone: str) -> StandardResponse:
   
   
    return StandardResponse(
        headers={"sender": "phone-service"},
        body={"processed": True, "query": phone},
        extra={"data_type": "phone"}
    )
from fastapi import APIRouter
from controllers.search_controller import router as search_router
from controllers.common_controller import router as common_router

api_router = APIRouter()
api_router.include_router(search_router, prefix="/domclick", tags=["domclick"])
api_router.include_router(common_router, prefix="/common", tags=["common"])
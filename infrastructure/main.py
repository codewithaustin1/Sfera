from fastapi import FastAPI
from api.v1.router import api_router

app = FastAPI(
    title="Sfera Refactored API",
    description="Refactored parsing services for Sfera system",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
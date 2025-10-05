from fastapi import FastAPI
from api.v1.router import api_router
from core.config import settings

app = FastAPI(
    title="Sfera Information System",
    description="Refactored parsing services for Sfera system - Migrated to Python",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Sfera Information System API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": settings.MODE}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
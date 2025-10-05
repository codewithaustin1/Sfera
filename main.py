"""
Main entry point for Sfera Information System
This file exists to maintain compatibility with existing deployment scripts
"""
from infrastructure.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("infrastructure.main:app", host="0.0.0.0", port=8000, reload=True)
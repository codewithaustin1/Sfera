import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    MODE: str = os.getenv("MODE", "dev")
    VALIDATOR_ENDPOINT: str = os.getenv("VALIDATOR_ENDPOINT", "http://localhost:8001")
    
settings = Settings()
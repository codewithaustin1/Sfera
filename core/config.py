import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    MODE: str = os.getenv("MODE", "dev")
    PROXY_URL: str = os.getenv("PROXY_URL", "")
    VALIDATOR_ENDPOINT: str = os.getenv("VALIDATOR_ENDPOINT", "")
    
settings = Settings()
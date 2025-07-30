import os
from typing import Optional
from dotenv import load_dotenv

class Settings:
    
    def __init__(self):
        load_dotenv()
        self.api_key: str = os.getenv("API_KEY")
        self.api_base_url: str = os.getenv("API_BASE_URL")

    
    @property
    def service_key(self) -> str:
        return self.api_key

settings = Settings() 
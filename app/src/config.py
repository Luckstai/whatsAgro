import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    nasa_api_key: str = os.getenv("NASA_API_KEY")

settings = Settings()

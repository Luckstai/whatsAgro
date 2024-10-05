import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    NASA_API_KEY: str = os.getenv("NASA_API_KEY")
    API_KEY_GPT: str = os.getenv("API_KEY_GPT")
    API_URL_GPT: str = os.getenv("API_URL_GPT")

settings = Settings()

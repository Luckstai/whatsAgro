import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    NASA_API_KEY: str = os.getenv("NASA_API_KEY")
    API_KEY_GPT: str = os.getenv("API_KEY_GPT")
    API_URL_GPT: str = os.getenv("API_URL_GPT")
    ASSISTANT_ID_GPT: str = os.getenv("ASSISTANT_ID_GPT")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME")
    RADIUS_KM: str = os.getenv("RADIUS_KM")
    TOKEN_EARTHDATA: str = os.getenv("TOKEN_EARTHDATA")
    AWS_ACCESS_KEY: str = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")

settings = Settings()

from pydantic import BaseModel


class EarthImageRequest(BaseModel):
    latitude: float
    longitude: float
    date: str  # Formato: YYYY-MM-DD

class EarthImageResponse(BaseModel):
    url: str

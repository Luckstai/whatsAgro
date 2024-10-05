from pydantic import BaseModel

class GIBSImageRequest(BaseModel):
    date: str  # Formato: YYYY-MM-DD
    bbox: str  # Bounding box: min_lon,min_lat,max_lon,max_lat

class GIBSImageResponse(BaseModel):
    image_data: bytes

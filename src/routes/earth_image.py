from fastapi import APIRouter, HTTPException
from src.schemas.earth_image import EarthImageRequest, EarthImageResponse
from src.services.nasa_api import get_earth_image
from src.shared.utils import validate_date

router = APIRouter(prefix="/earth_image", tags=["Earth Image"])

@router.post("/", response_model=EarthImageResponse)
def fetch_earth_image(request: EarthImageRequest):
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    try:
        data = get_earth_image(request.latitude, request.longitude, request.date)
        return EarthImageResponse(url=data.get("url", "No URL found"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
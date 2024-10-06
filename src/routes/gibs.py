# app/routes/gibs.py
from fastapi import APIRouter, HTTPException, Response
from src.schemas.gibs import GIBSImageRequest, GIBSImageResponse
from src.services.nasa_api import get_gibs_image
from src.shared.utils import validate_date

router = APIRouter(prefix="/gibs_image", tags=["GIBS Image"])

@router.post("/", response_class=Response)
def fetch_gibs_image(request: GIBSImageRequest):
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    try:
        image_data = get_gibs_image(request.date, request.bbox)
        return Response(content=image_data, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
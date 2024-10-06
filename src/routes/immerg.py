# app/routes/immerg.py
from fastapi import APIRouter, HTTPException
from src.schemas.immerg import IMERGDataRequest, IMERGDataResponse
from src.services.nasa_api import get_precipitation_data
from src.shared.utils import validate_date

router = APIRouter(prefix="/immerg_data", tags=["IMERG Data"])

#API de precipitação
@router.post("/", response_model=IMERGDataResponse)
def fetch_immerg_data(request: IMERGDataRequest):
    if not (validate_date(request.start_date) and validate_date(request.end_date)):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYYMMDD.")
    
    try:
        data = get_precipitation_data(request.start_date, request.end_date, request.latitude, request.longitude)
        return IMERGDataResponse(precipitation_data=data.get("properties", {}).get("parameter", {}).get("PRECTOT", {}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

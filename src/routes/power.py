from fastapi import APIRouter, HTTPException
from src.schemas.power import PowerDataRequest, PowerDataResponse
from src.services.nasa_api import get_power_data
from src.shared.utils import validate_date

router = APIRouter(prefix="/power_data", tags=["POWER Data"])

@router.post("/", response_model=PowerDataResponse)
def fetch_power_data(request: PowerDataRequest):
    if not (validate_date(request.start_date) and validate_date(request.end_date)):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYYMMDD.")
    
    try:
        data = get_power_data(request.latitude, request.longitude, request.start_date, request.end_date, request.parameters)
        return PowerDataResponse(data=data.get("properties", {}).get("parameter", {}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
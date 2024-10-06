from fastapi import APIRouter, HTTPException
from src.schemas.ecostress import EcostressDataRequest, EcostressDataResponse
from src.services.nasa_api import get_evapotranspiration_data
from src.shared.utils import validate_date

router = APIRouter(prefix="/ecostress_data", tags=["ECOSTRESS Data"])

@router.post("/", response_model=EcostressDataResponse)
def fetch_ecostress_data(request: EcostressDataRequest):
    if not (validate_date(request.start_date) and validate_date(request.end_date)):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYYMMDD.")
    
    try:
        data = get_evapotranspiration_data(request.latitude, request.longitude, request.start_date, request.end_date)
        return EcostressDataResponse(evapotranspiration_data=data.get("properties", {}).get("parameter", {}).get("EVAP", {}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
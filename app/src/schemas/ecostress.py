from typing import Dict
from pydantic import BaseModel

class EcostressDataRequest(BaseModel):
    latitude: float
    longitude: float
    start_date: str  # Formato: YYYYMMDD
    end_date: str    # Formato: YYYYMMDD

class EcostressDataResponse(BaseModel):
    evapotranspiration_data: Dict

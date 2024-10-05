from typing import Dict
from pydantic import BaseModel


class IMERGDataRequest(BaseModel):
    start_date: str  # Formato: YYYYMMDD
    end_date: str    # Formato: YYYYMMDD
    latitude: float
    longitude: float

class IMERGDataResponse(BaseModel):
    precipitation_data: Dict

from pydantic import BaseModel
from typing import Dict

class PowerDataRequest(BaseModel):
    latitude: float
    longitude: float
    start_date: str  # Formato: YYYYMMDD
    end_date: str    # Formato: YYYYMMDD
    parameters: str  # Ex: "T2M,PRECTOT"

class PowerDataResponse(BaseModel):
    data: Dict

from src.shared.s3.s3_service import get_latest_csv_from_s3
from fastapi import APIRouter, HTTPException
from datetime import datetime
import pandas as pd
import math

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# Função para calcular a distância entre dois pontos (latitude e longitude) usando a fórmula de Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # Distância em km
    
    return distance
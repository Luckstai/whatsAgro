import requests
from config import settings

NASA_API_KEY = settings.nasa_api_key


def get_earth_image(lat: float, lon: float, date: str):
    url = f'https://api.nasa.gov/planetary/earth/assets?lon={lon}&lat={lat}&date={date}&dim=0.1&api_key={NASA_API_KEY}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_gibs_image(date: str, bbox: str):
    url = f'https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/{date}/250m/4/8/8.jpg'
    response = requests.get(url, stream=True)
    response.raise_for_status()
    return response.content

def get_power_data(lat: float, lon: float, start_date: str, end_date: str, parameters: str):
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"start={start_date}&end={end_date}&latitude={lat}&longitude={lon}"
        f"&community=AG&parameters={parameters}&format=JSON&user={NASA_API_KEY}"
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_precipitation_data(lat: float, lon: float, start_date: str, end_date: str):
    return get_power_data(lat, lon, start_date, end_date, "PRECTOT")

def get_evapotranspiration_data(lat: float, lon: float, start_date: str, end_date: str):
    return get_power_data(lat, lon, start_date, end_date, "EVAP")

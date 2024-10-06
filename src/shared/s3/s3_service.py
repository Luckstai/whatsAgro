import boto3
import pandas as pd
from io import StringIO
from src.config import settings

S3_BUCKET_NAME = settings.S3_BUCKET_NAME
RADIUS_KM = settings.RADIUS_KM

def get_latest_csv_from_s3(bucket_name: str, prefix: str) -> pd.DataFrame:
    s3 = boto3.client('s3')

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if 'Contents' not in response:
        raise Exception(f"Nenhum arquivo encontrado no bucket {bucket_name} com o prefixo {prefix}")

    sorted_files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
    latest_file = sorted_files[0]

    csv_obj = s3.get_object(Bucket=bucket_name, Key=latest_file['Key'])
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')

    data = pd.read_csv(StringIO(csv_string))
    
    print(f"Arquivo mais recente: {latest_file['Key']}")
    return data

def get_farmer_data(lat: float, lon: float):
    try:

        prefix = "trusted/"
        data = get_latest_csv_from_s3(S3_BUCKET_NAME, prefix)

        # Encontrar registros dentro do raio especificado
        nearby_records = []
        for _, row in data.iterrows():
            record_lat = row['Latitude']
            record_lon = row['Longitude']
            distance = haversine(lat, lon, record_lat, record_lon)
            
            if distance <= RADIUS_KM:
                nearby_records.append(row)

        if nearby_records:
            return {"records": pd.DataFrame(nearby_records).to_dict(orient="records")}
        else:
            return {"message": f"Nenhum registro encontrado dentro de {radius_km} km."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
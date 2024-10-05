from fastapi import FastAPI
from routes import earth_image, gibs, power, immerg, ecostress, onboarding

app = FastAPI(
    title="NASA Agriculture Monitoring API",
    description="API para monitorar e gerenciar recursos hídricos agrícolas usando dados da NASA",
    version="1.0.0",
)

# Incluir as rotas
app.include_router(earth_image.router)
app.include_router(gibs.router)
app.include_router(power.router)
app.include_router(immerg.router)
app.include_router(ecostress.router)
app.include_router(onboarding.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à NASA Agriculture Monitoring API!"}



#run --> uvicorn main:app --reload
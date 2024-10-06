from fastapi import FastAPI
from src.routes import earth_image, gibs, power, immerg, ecostress, gpt, messages
from apscheduler.schedulers.background import BackgroundScheduler
from src.services.nasa_api import get_precipitation_data
from src.services.whatsapp import send_whatsapp_message
from datetime import datetime

app = FastAPI(
    title="NASA Agriculture Monitoring API",
    description="API para monitorar e gerenciar recursos hídricos agrícolas usando dados da NASA",
    version="1.0.0",
)

def check_nasa_and_send_alerts():
    print(f"[{datetime.now()}] Verificando dados da NASA...")
    
    # Exemplo de dados de localização dos agricultores
    farmers = [
        {"name": "Lima", "phone": "+5511974260532", "region": "Nordeste", "lat": -7.1195, "lon": -34.8450},
        {"name": "Macedo", "phone": "+5511959200060", "region": "Sul", "lat": -30.0346, "lon": -51.2177},
        {"name": "Lucas", "phone": "+5511999424963", "region": "Sul", "lat": -30.0346, "lon": -51.2177},
        {"name": "Matheus", "phone": "+5511977642485", "region": "Sul", "lat": -30.0346, "lon": -51.2177},
    ]
    
    # Iterar sobre cada agricultor
    for farmer in farmers:
        # Exemplo de chamada para verificar os dados da NASA (chuva)
        start_date = "20240101"
        end_date = "20240131"
        # precip_data = get_precipitation_data(farmer["lat"], farmer["lon"], start_date, end_date)

        # Se o valor de precipitação indicar seca, enviar alerta
        # for date, precip in precip_data.items():
        # if precip < 10:  # Exemplo de condição para definir seca
        message = f"Alerta de seca para {farmer['region']}! Precipitação baixa detectada."
        send_whatsapp_message(farmer["phone"], message)
        print(f"Alerta enviado para {farmer['name']} no número {farmer['phone']}")
        # else:
        #     print(f"Precipitação suficiente para {farmer['name']} em {date}: {precip} mm")
    
    print(f"[{datetime.now()}] Verificação concluída.")

# Função para iniciar o cron job
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_nasa_and_send_alerts, "interval", hours=1)  # Roda a cada 1 hora 
    # scheduler.add_job(check_nasa_and_send_alerts, "interval", minutes=1)  # Roda a cada 5 minutos
    scheduler.start()
    print("Cron job iniciado...")

# Iniciar o agendador quando a aplicação começar
@app.on_event("startup")
def startup_event():
    start_scheduler()

# Incluir as rotas
app.include_router(earth_image.router)
app.include_router(gibs.router)
app.include_router(power.router)
app.include_router(immerg.router)
app.include_router(ecostress.router)
app.include_router(gpt.router)
app.include_router(messages.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à NASA Agriculture Monitoring API!"}




# from services.gpt_api import ask_chatgpt


# # pergunta = "Qual é a capital da França?"
# pergunta = "Estou localizado em São Paulo, gostaria de saber quais as chances de chuva para os próximos dias?"
# pergunta = "Como está a umidade do solo hoje no Rio De Janeiro?"
# resposta = ask_chatgpt(pergunta)

# api_endpoint_config = {
#     ""
# }

# print(resposta)


#run --> uvicorn main:app --reload
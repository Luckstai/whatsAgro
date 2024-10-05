from fastapi import FastAPI
from routes import earth_image, gibs, power, immerg, ecostress, gpt

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
app.include_router(gpt.router)

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
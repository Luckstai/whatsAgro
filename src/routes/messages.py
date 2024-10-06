from fastapi import APIRouter, HTTPException, Form, Request

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/")
async def received_messages(request: Request):
    # Log ou processar a mensagem
    # Acessar os parâmetros enviados no corpo da requisição
    form_data = await request.form()
    
    # Logar cada parâmetro recebido
    for key, value in form_data.items():
        logging.info(f"{key}: {value}")
    
    # # Verificar se há mídia anexada
    # if int(NumMedia) > 0 and MediaUrl0 and MediaContentType0:
    #     print(f"Mídia recebida: {MediaUrl0}, Tipo: {MediaContentType0}")
    
    # Retornar um status de sucesso para Twilio
    return {"status": "success"}
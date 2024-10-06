from fastapi import APIRouter, HTTPException, Form

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/")
async def received_messages(
    From: str = Form(...),         # Número de quem enviou a mensagem
    Body: str = Form(...),         # O corpo da mensagem
    NumMedia: str = Form(...),     # Número de mídias anexadas (se houver)
    MediaUrl0: str = Form(None),   # URL da primeira mídia anexada (opcional)
    MediaContentType0: str = Form(None)  # Tipo de conteúdo da mídia (opcional)
):
    # Log ou processar a mensagem
    print(f"Mensagem recebida de {From}: {Body}")
    
    # Verificar se há mídia anexada
    if int(NumMedia) > 0 and MediaUrl0 and MediaContentType0:
        print(f"Mídia recebida: {MediaUrl0}, Tipo: {MediaContentType0}")
    
    # Retornar um status de sucesso para Twilio
    return {"status": "success"}
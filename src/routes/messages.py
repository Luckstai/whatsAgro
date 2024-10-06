from fastapi import APIRouter, HTTPException, Form, Request
from src.shared.s3.s3_service import get_farmer_data
router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/")
async def received_messages(request: Request):
    print('CHEGOU MENSAGEM')
    
    get_farmer_data(-23.618202209473, -46.499969482422)
    
    # consultar se para esse numero existe dasdoscadastrados
    
    # consultar s3
    
#LOCALIZAÇÃO
# Latitude: -23.618202209473
# Longitude: -46.499969482422
# SmsMessageSid: SM6f55c6d9124448fab79177abb108fcdb
# NumMedia: 0
# ProfileName: Lucas
# MessageType: location
# SmsSid: SM6f55c6d9124448fab79177abb108fcdb
# WaId: 5511999424963
# SmsStatus: received
# Body: 
# To: whatsapp:+14155238886
# NumSegments: 1
# ReferralNumMedia: 0
# MessageSid: SM6f55c6d9124448fab79177abb108fcdb
# AccountSid: AC92582b54a9b6d802c7be3fece551553c
# From: whatsapp:+5511999424963
# ApiVersion: 2010-04-01

#TEXTO
# SmsMessageSid: SMe5f4d558f4db0d513a8e1b3d2480022a
# NumMedia: 0
# ProfileName: Lucas
# MessageType: text
# SmsSid: SMe5f4d558f4db0d513a8e1b3d2480022a
# WaId: 5511999424963
# SmsStatus: received
# Body: Só texto
# To: whatsapp:+14155238886
# NumSegments: 1
# ReferralNumMedia: 0
# MessageSid: SMe5f4d558f4db0d513a8e1b3d2480022a
# AccountSid: AC92582b54a9b6d802c7be3fece551553c
# From: whatsapp:+5511999424963
# ApiVersion: 2010-04-01

    form_data = await request.form()
    
    # Logar cada parâmetro recebido
    for key, value in form_data.items():
        print(f"{key}: {value}")
    
    # # Verificar se há mídia anexada
    # if int(NumMedia) > 0 and MediaUrl0 and MediaContentType0:
    #     print(f"Mídia recebida: {MediaUrl0}, Tipo: {MediaContentType0}")
    
    # Retornar um status de sucesso para Twilio
    return {"status": "success"}
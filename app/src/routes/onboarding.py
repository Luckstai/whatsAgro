from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from firebase_admin import credentials, firestore
import firebase_admin
from twilio.twiml.messaging_response import MessagingResponse
from schemas.onboarding import OnboardingRequest

router = APIRouter(prefix="/whatsapp", tags=["Onboarding"])

# Inicializar o Firebase Admin SDK
cred = credentials.Certificate('../firebase_credentials.json')
firebase_admin.initialize_app(cred)

# Inicializar o Firestore Database
db = firestore.client()

# Endpoint para receber mensagens do WhatsApp
@router.post('/', response_class=JSONResponse)
def whatsapp(request: OnboardingRequest):
    # Receber dados do Twilio (número do agricultor e mensagem)
    data = request.json()  # Obtemos os dados da requisição JSON

    # Acessar os dados corretamente
    phone_number = data.get("from")
    message_body = data.get("body")

    # Limpar o número (remover prefixo 'whatsapp:')
    phone_number = phone_number.replace('whatsapp:', '')

    # Salvar a mensagem no Firestore
    save_message_to_firestore(phone_number, message_body)

    # Responder automaticamente
    resp = MessagingResponse()
    resp.message(f"Obrigado! Recebemos sua mensagem: {message_body}")

    return str(resp)

# Função para salvar mensagens no Firestore
def save_message_to_firestore(phone_number, message_body):
    doc_ref = db.collection('agricultores').document(phone_number)
    doc_ref.set({
        'telefone': phone_number,
        'mensagem': message_body
    })

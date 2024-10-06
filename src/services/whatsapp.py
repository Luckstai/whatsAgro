import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to: str, body: str):
    """
    Enviar mensagem de texto via WhatsApp usando Twilio.
    :param to: Número de telefone do destinatário no formato +5511999999999 (incluindo código do país).
    :param body: Conteúdo da mensagem.
    :return: SID da mensagem, ou None em caso de erro.
    """
    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=body,
            to=f'whatsapp:{to}'
        )
        print(f"Mensagem enviada para {to}. SID: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return None

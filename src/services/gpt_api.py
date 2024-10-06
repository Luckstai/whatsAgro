import requests
from src.config import settings

API_KEY_GPT = settings.API_KEY_GPT
API_URL_GPT = settings.API_URL_GPT

def get_gpt_response(question):
    headers = {
        'Authorization': f'Bearer {API_KEY_GPT}',
        'Content-Type': 'application/json'
    }

    assistente_1 =  {
        "role": "system", 
        "content": """
            Você é um assistente para ajudar agricultores a tomar melhores decisões a respeito dos dados fornecidos.
            Você deve responder apenas perguntas relacionadas ao clima, à agricultura ou umidade do solo e do ar.

            Temos 4 APIs e dependendo da sua interpretação do que o usuário quer, responda com o número da API que melhor corresponde ao assunto.

            API_1 - Responsável por receber informações do usuário referentes a localização e devolve a chance de chuva para os próximos meses naquela área ou a umidade do solo
            API_2 - Responsável por receber informações do usuário referentes a localização e tipo de plantio e devolve qual seria o melhor tipo de plantação para aquela área na data atual
            
            A resposta deve conter apenas uma das opções: API_1, API_2
        """
        }

    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
           assistente_1,
            {'role': 'user', 'content': question}
        ],
        'max_tokens': 150  # Limite de tokens para a resposta
    }

    try:
        response = requests.post(API_URL_GPT, headers=headers, json=data)
        response.raise_for_status()

        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print("GPT quota exceeded. Please check your plan.")
        else:
            print(f"An error occurred: {e}")

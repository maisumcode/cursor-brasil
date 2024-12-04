import requests
import json
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def consultar_gemini(pergunta):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-8b:generateContent"
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Verifica se a chave API foi carregada
    if not api_key:
        return "Erro: Chave API não encontrada no arquivo .env"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    pergunta_formatada = f"Responda em português do Brasil de forma direta e objetiva: {pergunta}"
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": pergunta_formatada
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        }
    }
    
    response = requests.post(
        f"{url}?key={api_key}",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        resposta_json = response.json()
        try:
            texto_resposta = resposta_json['candidates'][0]['content']['parts'][0]['text']
            return texto_resposta.strip()
        except (KeyError, IndexError):
            return "Erro ao processar a resposta do Gemini"
    else:
        return f"Erro na requisição: {response.status_code} - {response.text}"

if __name__ == "__main__":
    print("=== Pesquisa Iniciada ===")
    print("------------------------")
    
    while True:
        pergunta = input("> ")
        if pergunta.lower() == "s":
            print("Pesquisa Encerrada.")
            break
        resposta = consultar_gemini(pergunta)
        print(resposta)
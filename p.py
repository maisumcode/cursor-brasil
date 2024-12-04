import requests
import json
import os
from dotenv import load_dotenv
from colors import Colors
from datetime import datetime

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def consultar_gemini(pergunta, historico=[]):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        return "Erro: Chave API não encontrada no arquivo .env"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Formata o contexto histórico com a pergunta atual
    conteudo = ""
    for msg in historico[-5:]:  # Mantém apenas as últimas 5 mensagens do histórico
        conteudo += msg + "\n"
    
    # Adiciona a pergunta atual
    pergunta_formatada = f"""{conteudo}
Você é um assistente especializado em informações atualizadas do Brasil.
IMPORTANTE: 
- Busque informações oficiais e atualizadas
- Foque em fontes como Banco Central e grandes portais de notícias
- Seja direto e objetivo

Pergunta: {pergunta}"""
    
    data = {
        "contents": [{
            "parts": [{
                "text": pergunta_formatada
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        }
    }
    
    if not pergunta.strip():
        return "Erro: A pergunta não pode estar vazia."

    try:
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=data
        )
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão: {e}"
    
    if response.status_code == 200:
        resposta_json = response.json()
        try:
            texto_resposta = resposta_json['candidates'][0]['content']['parts'][0]['text']
            return texto_resposta.strip()
        except (KeyError, IndexError):
            return "Erro ao processar a resposta do Gemini"
    else:
        return f"Erro na requisição: {response.status_code} - {response.text}"

def buscar_na_web(query):
    subscription_key = os.getenv('BING_SEARCH_V7_SUBSCRIPTION_KEY')
    endpoint = os.getenv('BING_SEARCH_V7_ENDPOINT') + "/bing/v7.0/search"
    
    if not subscription_key or not endpoint:
        return "Erro: Chave de assinatura ou endpoint não configurados."

    params = {'q': query, 'mkt': 'pt-BR'}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        resultados = response.json()
        return resultados
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão: {e}"

def obter_data_hora_atual():
    agora = datetime.now()
    data_hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
    return data_hora_formatada

if __name__ == "__main__":
    print(f"{Colors.HEADER}=== Pesquisa Iniciada ==={Colors.END}")
    print(f"{Colors.GRAY}------------------------{Colors.END}")
    
    historico_conversa = []
    
    while True:
        pergunta = input(f"{Colors.GREEN}> {Colors.END}")
        if pergunta.lower() == "s":
            print(f"{Colors.WARNING}Pesquisa Encerrada.{Colors.END}")
            break
            
        if "data" in pergunta.lower() or "hora" in pergunta.lower():
            resposta = obter_data_hora_atual()
        else:
            resposta_gemini = consultar_gemini(pergunta, historico_conversa)
            resposta_web = buscar_na_web(pergunta)
            resposta = f"Resposta Gemini: {resposta_gemini}\nResultados da Web: {resposta_web}"
        
        print(f"{Colors.CYAN}{resposta}{Colors.END}")
        
        if "Erro" not in resposta:
            historico_conversa.append(f"Usuário: {pergunta}")
            historico_conversa.append(f"Assistente: {resposta}")
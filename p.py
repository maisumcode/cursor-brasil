import requests
import json
import os
from dotenv import load_dotenv
from colors import Colors
from datetime import datetime
from bs4 import BeautifulSoup

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

    params = {'q': query}
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

def buscar_informacoes_bitcoin():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'brl,usd',
        'include_24hr_change': 'true'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        dados = response.json()
        
        preco_brl = dados['bitcoin']['brl']
        preco_usd = dados['bitcoin']['usd']
        variacao_24h = dados['bitcoin'].get('brl_24h_change', 0)
        
        return f"Bitcoin: R$ {preco_brl:,.2f} | US$ {preco_usd:,.2f} | 24h: {variacao_24h:.2f}%"
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão: {e}"
    except Exception as e:
        return f"Erro ao processar dados: {e}"

def main():
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
        elif "bitcoin" in pergunta.lower():
            resposta = buscar_informacoes_bitcoin()
        else:
            resposta_gemini = consultar_gemini(pergunta, historico_conversa)
            if "Erro" in resposta_gemini or "não tenho acesso à internet" in resposta_gemini.lower():
                resposta_web = buscar_na_web(pergunta)
                resposta = resposta_web
            else:
                resposta = resposta_gemini
        
        print(f"{Colors.CYAN}{resposta}{Colors.END}")
        
        if "Erro" not in resposta:
            historico_conversa.append(f"Usuário: {pergunta}")
            historico_conversa.append(f"Assistente: {resposta}")

if __name__ == "__main__":
    main()
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def buscar_na_web(query: str) -> str:
    """
    Realiza uma busca na web usando a API do Bing.
    
    Args:
        query: Termo de busca
        
    Returns:
        str: Resultados formatados da busca
    """
    subscription_key = os.getenv('BING_SEARCH_V7_SUBSCRIPTION_KEY')
    endpoint = os.getenv('BING_SEARCH_V7_ENDPOINT') + "/bing/v7.0/search"
    
    if not subscription_key or not endpoint:
        return "Erro: Chave de assinatura ou endpoint não configurados."

    params = {'q': query, 'mkt': 'pt-BR', 'count': 5}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        resultados = response.json()
        
        if 'webPages' in resultados and 'value' in resultados['webPages']:
            texto_resposta = "Aqui está o que encontrei:\n\n"
            for item in resultados['webPages']['value'][:3]:
                texto_resposta += f"• {item['name']}\n"
                texto_resposta += f"{item['snippet']}\n\n"
            return texto_resposta
        return "Não encontrei resultados relevantes para sua pesquisa."
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão: {e}" 
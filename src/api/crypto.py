import requests
from typing import Dict, Any

def buscar_informacoes_cripto(cripto_id: str = 'bitcoin') -> str:
    """
    Busca informações de criptomoedas na API do CoinGecko.
    
    Args:
        cripto_id: ID da criptomoeda (ex: 'bitcoin', 'ethereum', 'flow')
        
    Returns:
        str: Informações formatadas sobre a criptomoeda
    """
    cripto_map = {
        'bitcoin': 'bitcoin',
        'ethereum': 'ethereum',
        'flow': 'flow',
        'bnb': 'binancecoin',
        'cardano': 'cardano',
        'solana': 'solana',
        'token flow': 'flow',
        'flow token': 'flow'
    }
    
    cripto_id = cripto_map.get(cripto_id.lower(), cripto_id.lower())
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': cripto_id,
        'vs_currencies': 'brl,usd',
        'include_24hr_change': 'true'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        dados = response.json()
        
        if cripto_id not in dados:
            return f"Erro: Criptomoeda {cripto_id} não encontrada"
        
        from ..utils.formatters import formatar_dados_cripto
        return formatar_dados_cripto(dados[cripto_id])
        
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão: {e}"
    except Exception as e:
        return f"Erro ao processar dados: {e}" 
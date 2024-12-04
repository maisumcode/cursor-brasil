import requests
import json
import os
from dotenv import load_dotenv
from colors import Colors
from datetime import datetime
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
import pandas as pd
import numpy as np
from typing import List, Dict, Optional

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
Você é um assistente inteligente e prestativo.
IMPORTANTE: 
- Seja direto e objetivo
- Forneça informações precisas e atualizadas
- Use fontes confiáveis quando necessário

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

def obter_data_hora_atual():
    agora = datetime.now()
    data_hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
    return data_hora_formatada

def buscar_informacoes_cripto(cripto_id='bitcoin'):
    """
    Busca informações de criptomoedas na API do CoinGecko
    
    Args:
        cripto_id (str): ID da criptomoeda (ex: 'bitcoin', 'ethereum', 'flow')
    """
    # Mapeamento de nomes comuns para IDs do CoinGecko
    cripto_map = {
        'bitcoin': 'bitcoin',
        'ethereum': 'ethereum',
        'flow': 'flow',
        'token flow': 'flow',
        'flow token': 'flow'
    }
    
    # Tenta encontrar o ID correto
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
        
        preco_brl = dados[cripto_id]['brl']
        preco_usd = dados[cripto_id]['usd']
        variacao_24h = dados[cripto_id].get('brl_24h_change', 0)
        
        # Cria DataFrame com os dados
        df = pd.DataFrame([
            ['Preço BRL', f"R$ {preco_brl:,.2f}"],
            ['Preço USD', f"US$ {preco_usd:,.2f}"],
            ['Variação 24h', f"{variacao_24h:.2f}%"],
            ['Média (BRL/USD)', f"R$ {((preco_brl + preco_usd * 5) / 2):,.2f}"],
            ['Diferença %', f"{((preco_brl / (preco_usd * 5) - 1) * 100):.2f}%"]
        ], columns=['Métrica', 'Valor'])
        
        # Formata tabela
        tabela = tabulate(
            df,
            headers='keys',
            tablefmt="pipe",
            stralign="left",
            showindex=False,
            numalign="right"
        )
        return tabela
        
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão: {e}"
    except Exception as e:
        return f"Erro ao processar dados: {e}"

def formatar_resposta(texto: str) -> str:
    """
    Formata o texto de resposta, convertendo tabelas para um formato mais legível
    usando pandas e tabulate.
    
    Args:
        texto (str): Texto contendo possíveis tabelas delimitadas por pipes
        
    Returns:
        str: Texto formatado com tabelas estilizadas
    """
    # Remove asteriscos
    texto = texto.replace('*', '')
    
    # Separa o texto em linhas
    linhas = texto.split('\n')
    
    # Encontra a última tabela no texto
    ultima_tabela_inicio = -1
    ultima_tabela_fim = -1
    i = 0
    
    # Detecta a última tabela no texto
    while i < len(linhas):
        linha = linhas[i].strip()
        if '|' in linha and not linha.startswith('>'):
            inicio_tabela = i
            while i < len(linhas) and '|' in linhas[i]:
                i += 1
            ultima_tabela_inicio = inicio_tabela
            ultima_tabela_fim = i
        i += 1
    
    # Se encontrou uma tabela, processa usando pandas
    if ultima_tabela_inicio >= 0:
        # Extrai as linhas da tabela
        linhas_tabela = [
            linha.strip() 
            for linha in linhas[ultima_tabela_inicio:ultima_tabela_fim] 
            if linha.strip() and not linha.startswith('>')
        ]
        
        # Converte para DataFrame
        try:
            # Extrai cabeçalho e dados
            header = [col.strip() for col in linhas_tabela[0].split('|') if col.strip()]
            dados = []
            
            for linha in linhas_tabela[1:]:
                if not all('-' in col for col in linha.split('|')):
                    colunas = [col.strip() for col in linha.split('|') if col.strip()]
                    if len(colunas) == len(header):
                        dados.append(colunas)
            
            # Cria DataFrame
            df = pd.DataFrame(dados, columns=header)
            
            # Formata usando tabulate com estilos
            tabela_formatada = tabulate(
                df,
                headers=header,
                tablefmt="pipe",
                stralign="left",
                showindex=False
            )
            
            # Aplica cores
            linhas_formatadas = tabela_formatada.split('\n')
            tabela_colorida = []
            
            # Formata cabeçalho
            tabela_colorida.append(f"{Colors.GREEN}{Colors.BOLD}{linhas_formatadas[0]}{Colors.END}")
            # Formata separador
            tabela_colorida.append(f"{Colors.GRAY}{linhas_formatadas[1]}{Colors.END}")
            
            # Formata dados
            for linha in linhas_formatadas[2:]:
                partes = linha.split('|')
                linha_colorida = []
                for k, parte in enumerate(partes):
                    if k == 1:  # Primeira coluna após pipe inicial
                        linha_colorida.append(f"{Colors.BLACK}{Colors.BOLD}{parte}{Colors.END}")
                    else:
                        linha_colorida.append(f"{Colors.CYAN}{parte}{Colors.END}")
                tabela_colorida.append('|'.join(linha_colorida))
            
            # Substitui a tabela original
            linhas[ultima_tabela_inicio:ultima_tabela_fim] = tabela_colorida
            
        except Exception as e:
            print(f"Erro ao processar tabela: {e}")
    
    # Processa outras linhas
    for i, linha in enumerate(linhas):
        if not '|' in linha:
            if not ':' in linha and i == 0:
                linhas[i] = f"{Colors.BLUE}{Colors.BOLD}{linha}{Colors.END}"
            elif ':' in linha:
                antes, depois = linha.split(':', 1)
                linhas[i] = f"{Colors.BLACK}{Colors.BOLD}{antes}:{Colors.END}{Colors.CYAN}{depois}{Colors.END}"
            elif linha.strip() and linha.strip()[0].isdigit() and '. ' in linha:
                numero, resto = linha.split('. ', 1)
                linhas[i] = f"{Colors.BLACK}{Colors.BOLD}{numero}. {Colors.END}{Colors.CYAN}{resto}{Colors.END}"
    
    # Remove linhas vazias e junta o resultado
    return '\n'.join(linha for linha in linhas if linha.strip())

def criar_dataframe_from_texto(texto: str) -> Optional[pd.DataFrame]:
    """
    Converte texto contendo tabela em DataFrame pandas.
    
    Args:
        texto (str): Texto contendo tabela delimitada por pipes
        
    Returns:
        Optional[pd.DataFrame]: DataFrame ou None se não houver tabela válida
    """
    try:
        linhas = [l.strip() for l in texto.split('\n') if '|' in l and not l.startswith('>')]
        if not linhas:
            return None
            
        header = [col.strip() for col in linhas[0].split('|') if col.strip()]
        dados = []
        
        for linha in linhas[1:]:
            if not all('-' in col for col in linha.split('|')):
                colunas = [col.strip() for col in linha.split('|') if col.strip()]
                if len(colunas) == len(header):
                    dados.append(colunas)
                    
        return pd.DataFrame(dados, columns=header)
    except Exception:
        return None

def analisar_historico(historico_conversa):
    """Analisa o histórico de conversas usando pandas"""
    # Converte histórico em DataFrame
    df = pd.DataFrame([
        {
            'tipo': msg.split(': ')[0],
            'mensagem': msg.split(': ')[1],
            'tamanho': len(msg.split(': ')[1])
        }
        for msg in historico_conversa
    ])
    
    # Análise básica
    analise = {
        'Total de mensagens': len(df),
        'Média de caracteres': df['tamanho'].mean(),
        'Maior mensagem': df['tamanho'].max(),
        'Mensagens do usuário': len(df[df['tipo'] == 'Usuário']),
        'Mensagens do assistente': len(df[df['tipo'] == 'Assistente'])
    }
    
    # Formata resultado
    tabela = tabulate(
        [[k, v] for k, v in analise.items()],
        headers=['Métrica', 'Valor'],
        tablefmt='pipe'
    )
    
    return tabela

def analisar_bitcoin(dados):
    """Analisa dados do Bitcoin usando numpy"""
    precos = np.array([
        dados['bitcoin']['brl'],
        dados['bitcoin']['usd']
    ])
    
    analise = {
        'Média': np.mean(precos),
        'Desvio': np.std(precos),
        'Variação': dados['bitcoin'].get('brl_24h_change', 0)
    }
    
    return tabulate(
        [[k, f"{v:.2f}"] for k, v in analise.items()],
        headers=['Métrica', 'Valor'],
        tablefmt='pipe'
    )

def main():
    print(f"{Colors.GREEN}=== Pesquisa Iniciada ==={Colors.END}")
    print(f"{Colors.GRAY}------------------------{Colors.END}")
    
    historico_conversa = []
    
    while True:
        pergunta = input(f"{Colors.GREEN}> {Colors.END}")
        if pergunta.lower() in ["s", "sair"]:
            break
            
        if pergunta.lower() in ["que horas são", "hora atual", "que hora é", "data atual", "que dia é hoje"]:
            resposta = obter_data_hora_atual()
        elif any(token in pergunta.lower() for token in ['bitcoin', 'ethereum', 'flow', 'bnb', 'cardano', 'solana']):
            # Extrai o nome da cripto da pergunta
            for token in ['bitcoin', 'ethereum', 'flow', 'bnb', 'cardano', 'solana']:
                if token in pergunta.lower():
                    cripto = token
                    break
            resposta = buscar_informacoes_cripto(cripto)
            resposta = formatar_resposta(resposta)
        elif pergunta.lower() == "estatísticas":
            resposta = analisar_historico(historico_conversa)
        else:
            resposta_gemini = consultar_gemini(pergunta, historico_conversa)
            if ("Erro" in resposta_gemini or 
                "não tenho acesso" in resposta_gemini.lower() or 
                "não posso fornecer" in resposta_gemini.lower()):
                print(f"{Colors.GRAY}Buscando informações na web...{Colors.END}")
                resposta = buscar_na_web(pergunta)
            else:
                resposta = formatar_resposta(resposta_gemini)
        
        print(f"{Colors.CYAN}{resposta}{Colors.END}")
        
        if "Erro" not in resposta:
            historico_conversa.append(f"Usuário: {pergunta}")
            historico_conversa.append(f"Assistente: {resposta}")

if __name__ == "__main__":
    main()
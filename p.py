import requests
import json
import os
from dotenv import load_dotenv
from colors import Colors
from datetime import datetime
from bs4 import BeautifulSoup
import re
from tabulate import tabulate

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

def formatar_resposta(texto):
    # Remove asteriscos
    texto = texto.replace('*', '')
    
    # Separa o texto em linhas
    linhas = texto.split('\n')
    
    # Encontra a última tabela no texto
    ultima_tabela_inicio = -1
    ultima_tabela_fim = -1
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        if '|' in linha and not linha.startswith('>'):
            inicio_tabela = i
            # Encontra o fim da tabela atual
            while i < len(linhas) and '|' in linhas[i]:
                i += 1
            fim_tabela = i
            # Atualiza os índices da última tabela encontrada
            ultima_tabela_inicio = inicio_tabela
            ultima_tabela_fim = fim_tabela
        i += 1
    
    # Se encontrou uma tabela, processa apenas a última
    if ultima_tabela_inicio >= 0:
        tabela_linhas = []
        headers = []
        
        # Processa apenas as linhas da última tabela
        for i in range(ultima_tabela_inicio, ultima_tabela_fim):
            linha_atual = linhas[i].strip()
            if linha_atual and not linha_atual.startswith('>'):
                colunas = [col.strip() for col in linha_atual.split('|') if col.strip()]
                
                if not headers and not all('-' in col for col in colunas):
                    headers = colunas
                elif not all('-' in col for col in colunas):
                    tabela_linhas.append(colunas)
        
        # Formata a tabela usando tabulate
        if headers and tabela_linhas:
            tabela_formatada = tabulate(
                tabela_linhas,
                headers=headers,
                tablefmt="pipe",
                stralign="left",
                colalign=["left"] * len(headers)
            )
            
            # Aplica cores na tabela formatada
            linhas_tabela = tabela_formatada.split('\n')
            tabela_colorida = []
            for j, linha_tab in enumerate(linhas_tabela):
                if j == 0:  # Cabeçalho
                    tabela_colorida.append(f"{Colors.GREEN}{Colors.BOLD}{linha_tab}{Colors.END}")
                elif j == 1:  # Linha separadora
                    tabela_colorida.append(f"{Colors.GRAY}{linha_tab}{Colors.END}")
                else:  # Conteúdo
                    partes = linha_tab.split('|')
                    linha_colorida = []
                    for k, parte in enumerate(partes):
                        if k == 1:  # Primeira coluna (após pipe inicial)
                            linha_colorida.append(f"{Colors.BLACK}{Colors.BOLD}{parte}{Colors.END}")
                        else:
                            linha_colorida.append(f"{Colors.CYAN}{parte}{Colors.END}")
                    tabela_colorida.append('|'.join(linha_colorida))
            
            # Substitui a tabela original pela formatada
            linhas[ultima_tabela_inicio:ultima_tabela_fim] = tabela_colorida
    
    # Processa as linhas não-tabela normalmente
    for i, linha in enumerate(linhas):
        if not '|' in linha:  # Processa apenas linhas que não são parte de tabela
            if not ':' in linha and i == 0:
                linhas[i] = f"{Colors.BLUE}{Colors.BOLD}{linha}{Colors.END}"
            elif ':' in linha:
                antes, depois = linha.split(':', 1)
                linhas[i] = f"{Colors.BLACK}{Colors.BOLD}{antes}:{Colors.END}{Colors.CYAN}{depois}{Colors.END}"
            elif linha.strip() and linha.strip()[0].isdigit() and '. ' in linha:
                numero, resto = linha.split('. ', 1)
                linhas[i] = f"{Colors.BLACK}{Colors.BOLD}{numero}. {Colors.END}{Colors.CYAN}{resto}{Colors.END}"
    
    # Junta as linhas novamente
    texto_formatado = '\n'.join(linha for linha in linhas if linha.strip())
    return texto_formatado

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
        elif "bitcoin" in pergunta.lower():
            resposta = buscar_informacoes_bitcoin()
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
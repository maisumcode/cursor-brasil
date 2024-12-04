import os
import requests
from typing import List
from dotenv import load_dotenv
from ..utils.colors import Colors

load_dotenv()

def formatar_resposta(texto: str) -> str:
    """
    Formata o texto da resposta com cores e estilos.
    """
    linhas = texto.split('\n')
    texto_formatado = []
    contador_topicos = 0
    
    for linha in linhas:
        # Formata títulos principais com **
        if linha.startswith('**') and linha.endswith('**'):
            titulo = linha.replace('**', '')
            linha = f"{Colors.BLUE}{titulo}{Colors.END}"
        
        # Formata perguntas (linhas que terminam com ?)
        elif linha.strip().endswith('?'):
            linha = f"{Colors.MAGENTA}{linha}{Colors.END}"
        
        # Formata tópicos com * no início
        elif linha.strip().startswith('*'):
            contador_topicos += 1
            texto = linha.replace('*', '').strip()
            
            # Se tem dois pontos, divide e formata diferente
            if ':' in texto:
                antes, depois = texto.split(':', 1)
                linha = f"{Colors.YELLOW}{contador_topicos}. {antes}{Colors.END}: {Colors.CYAN}{depois}{Colors.END}"
            else:
                linha = f"{Colors.YELLOW}{contador_topicos}. {Colors.CYAN}{texto}{Colors.END}"
        
        # Formata linhas com dois pontos no meio
        elif ':' in linha and not linha.startswith(('http://', 'https://')):
            antes, depois = linha.split(':', 1)
            linha = f"{Colors.GREEN}{antes}{Colors.END}:{Colors.CYAN}{depois}{Colors.END}"
        
        # Formata texto normal
        else:
            linha = f"{Colors.CYAN}{linha}{Colors.END}"
            
        texto_formatado.append(linha)
    
    return '\n'.join(texto_formatado)

def consultar_gemini(pergunta: str, historico: List[str] = []) -> str:
    """
    Consulta a API do Gemini com uma pergunta e histórico opcional.
    
    Args:
        pergunta: Pergunta a ser enviada para o Gemini
        historico: Lista opcional de mensagens anteriores
        
    Returns:
        str: Resposta do modelo Gemini
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        return "Erro: Chave API não encontrada no arquivo .env"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    conteudo = ""
    for msg in historico[-5:]:
        conteudo += msg + "\n"
    
    pergunta_formatada = f"""{conteudo}
Você é um assistente inteligente e prestativo.
IMPORTANTE: 
- Seja direto e objetivo
- Forneça informações precisas e atualizadas
- Use fontes confiáveis quando necessário
- Use '**Título**' para títulos principais
- Use '*' no início para listar tópicos
- Coloque dois pontos ':' após labels ou categorias

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
            return formatar_resposta(texto_resposta.strip())
        except (KeyError, IndexError):
            return "Erro ao processar a resposta do Gemini"
    else:
        return f"Erro na requisição: {response.status_code} - {response.text}" 
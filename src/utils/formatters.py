from datetime import datetime
import pandas as pd
from tabulate import tabulate
from typing import Dict, Any
from .colors import Colors

def formatar_dados_cripto(dados: Dict[str, Any]) -> str:
    """
    Formata os dados de criptomoeda em uma tabela colorida.
    
    Args:
        dados: Dicionário com dados da criptomoeda
        
    Returns:
        str: Tabela formatada com os dados
    """
    preco_brl = dados['brl']
    preco_usd = dados['usd']
    variacao_24h = dados.get('brl_24h_change', 0)
    
    # Formata os valores com cores
    valores = [
        ['Preço BRL', f"{Colors.CYAN}R$ {preco_brl:,.2f}{Colors.END}"],
        ['Preço USD', f"{Colors.CYAN}US$ {preco_usd:,.2f}{Colors.END}"],
        ['Variação 24h', f"{Colors.CYAN}{variacao_24h:.2f}%{Colors.END}"],
        ['Média (BRL/USD)', f"{Colors.CYAN}R$ {((preco_brl + preco_usd * 5) / 2):,.2f}{Colors.END}"],
        ['Diferença %', f"{Colors.CYAN}{((preco_brl / (preco_usd * 5) - 1) * 100):.2f}%{Colors.END}"]
    ]
    
    # Cria o DataFrame com as cores
    df = pd.DataFrame(valores, columns=[
        f"{Colors.GREEN}Métrica{Colors.END}",
        f"{Colors.GREEN}Valor{Colors.END}"
    ])
    
    # Formata a tabela com cores nas bordas
    tabela = tabulate(
        df,
        headers='keys',
        tablefmt="pipe",
        stralign="left",
        showindex=False,
        numalign="right"
    )
    
    # Adiciona cores às linhas da tabela
    linhas = tabela.split('\n')
    linhas_coloridas = []
    
    for i, linha in enumerate(linhas):
        if i == 1:  # Linha separadora
            linha = f"{Colors.GRAY}{linha}{Colors.END}"
        elif '|' in linha:  # Linhas de dados
            partes = linha.split('|')
            linha = f"{Colors.RED}|{Colors.END}".join(partes)
        linhas_coloridas.append(linha)
    
    return '\n'.join(linhas_coloridas)

def obter_data_hora_atual() -> str:
    """Retorna a data e hora atual formatada."""
    agora = datetime.now()
    return agora.strftime("%d/%m/%Y %H:%M:%S") 
import os
from datetime import datetime
from ..utils.colors import Colors

class HistoricoChat:
    def __init__(self):
        # Pega o diretório raiz do projeto
        self.projeto_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.historico_dir = os.path.join(self.projeto_dir, "historico")
        self.criar_diretorio()

    def criar_diretorio(self):
        """Cria o diretório de histórico se não existir."""
        if not os.path.exists(self.historico_dir):
            os.makedirs(self.historico_dir)
            print(f"Diretório de histórico criado em: {self.historico_dir}")

    def limpar_texto(self, texto):
        """
        Remove códigos de escape ANSI e outros caracteres especiais do texto.
        """
        import re
        # Remove códigos de escape ANSI (incluindo cores)
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        texto = ansi_escape.sub('', texto)
        
        # Remove caracteres especiais ESC
        texto = texto.replace('\x1b', '')
        
        # Remove códigos como [0;34m, [0m, etc
        texto = re.sub(r'\[[0-9;]*m', '', texto)
        
        return texto.strip()

    def salvar_conversa(self, historico_conversa):
        """
        Salva apenas a última interação da conversa em um arquivo MDX.
        """
        if not historico_conversa or len(historico_conversa) < 2:
            return
            
        data_atual = datetime.now()
        nome_arquivo = f"chat_{data_atual.strftime('%Y%m%d_%H%M%S')}.mdx"
        caminho_arquivo = os.path.join(self.historico_dir, nome_arquivo)
        
        # Pega apenas a última interação
        ultima_pergunta = self.limpar_texto(historico_conversa[-2].replace("Usuário: ", ""))
        ultima_resposta = self.limpar_texto(historico_conversa[-1].replace("Assistente: ", ""))
        
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            # Frontmatter MDX
            f.write("---\n")
            f.write(f"title: 'Chat {data_atual.strftime('%d/%m/%Y')}'\n")
            f.write(f"date: '{data_atual.strftime('%Y-%m-%d')}'\n")
            f.write(f"time: '{data_atual.strftime('%H:%M:%S')}'\n")
            f.write("type: 'chat'\n")
            f.write("---\n\n")
            
            # Salva apenas a última interação
            f.write(f"## Pergunta\n{ultima_pergunta}\n\n")
            f.write(f"## Resposta\n{ultima_resposta}\n\n")
            f.write("---\n\n")

        print(f"\n{Colors.YELLOW}Histórico salvo em:{Colors.END}")
        print(f"{Colors.CYAN}{caminho_arquivo}{Colors.END}\n")

    def carregar_ultimo_historico(self):
        """
        Carrega o último arquivo de histórico.
        """
        if not os.path.exists(self.historico_dir):
            return "Nenhum histórico encontrado."
            
        arquivos = os.listdir(self.historico_dir)
        arquivos_mdx = [f for f in arquivos if f.endswith('.mdx')]
        
        if not arquivos_mdx:
            return "Nenhum histórico encontrado."
            
        ultimo_arquivo = sorted(arquivos_mdx)[-1]
        
        with open(f"{self.historico_dir}/{ultimo_arquivo}", "r", encoding="utf-8") as f:
            conteudo = f.read()
            
        return conteudo

    def formatar_historico(self, historico_conversa, mostrar_ultimo=False):
        """
        Formata o histórico de conversas.
        """
        if not historico_conversa:
            return "Ainda não temos histórico de conversas."
        
        if mostrar_ultimo and len(historico_conversa) >= 2:
            ultima_pergunta = historico_conversa[-2].replace("Usuário: ", "")
            ultima_resposta = historico_conversa[-1].replace("Assistente: ", "")
            
            resposta = f"\n{Colors.BLUE}Último assunto discutido:{Colors.END}\n\n"
            resposta += f"{Colors.GREEN}Pergunta:{Colors.END} {ultima_pergunta}\n"
            resposta += f"{Colors.CYAN}Resposta:{Colors.END} {ultima_resposta}\n"
            return resposta
        
        resposta = f"\n{Colors.BLUE}Histórico do Chat:{Colors.END}\n\n"
        data_atual = datetime.now().strftime("%d/%m/%Y")
        hora_atual = datetime.now().strftime("%H:%M:%S")
        
        resposta += f"{Colors.YELLOW}Data:{Colors.END} {data_atual}\n"
        resposta += f"{Colors.YELLOW}Hora:{Colors.END} {hora_atual}\n\n"
        
        for i in range(0, len(historico_conversa), 2):
            if i + 1 < len(historico_conversa):
                pergunta = historico_conversa[i].replace("Usuário: ", "")
                resposta_hist = historico_conversa[i + 1].replace("Assistente: ", "")
                
                resposta += f"{Colors.GREEN}Pergunta:{Colors.END} {pergunta}\n"
                resposta += f"{Colors.CYAN}Resposta:{Colors.END} {resposta_hist}\n\n"
        
        return resposta 
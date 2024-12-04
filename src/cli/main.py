from ..api import gemini, bing, crypto
from ..utils.colors import Colors
from ..utils import formatters
from ..utils.historico import HistoricoChat

def main():
    print(f"{Colors.GREEN}=== Pesquisa Iniciada ==={Colors.END}")
    print(f"{Colors.GRAY}------------------------{Colors.END}")
    
    historico_conversa = []
    historico = HistoricoChat()
    
    while True:
        pergunta = input(f"{Colors.GREEN}> {Colors.END}")
        if pergunta.lower() in ["s", "sair"]:
            # Salva o histórico antes de sair
            historico.salvar_conversa(historico_conversa)
            break
            
        if pergunta.lower() in ["que horas são", "hora atual", "que hora é", "data atual", "que dia é hoje"]:
            resposta = formatters.obter_data_hora_atual()
        elif any(termo in pergunta.lower() for termo in [
            "historico", "histórico", "histórico do chat", "historico do chat",
            "sabe o historico", "sabe o histórico"
        ]):
            resposta = historico.formatar_historico(historico_conversa, mostrar_ultimo=False)
        elif any(termo in pergunta.lower() for termo in [
            "qual foi o assunto", "o que falamos", "ultima conversa",
            "último assunto", "falamos a ultima vez", "assunto anterior"
        ]):
            resposta = historico.formatar_historico(historico_conversa, mostrar_ultimo=True)
        elif any(token in pergunta.lower() for token in ['bitcoin', 'ethereum', 'flow', 'bnb', 'cardano', 'solana']):
            for token in ['bitcoin', 'ethereum', 'flow', 'bnb', 'cardano', 'solana']:
                if token in pergunta.lower():
                    cripto = token
                    break
            resposta = crypto.buscar_informacoes_cripto(cripto)
        else:
            resposta_gemini = gemini.consultar_gemini(pergunta, historico_conversa)
            if ("Erro" in resposta_gemini or 
                "não tenho acesso" in resposta_gemini.lower() or 
                "não posso fornecer" in resposta_gemini.lower()):
                print(f"{Colors.GRAY}Buscando informações na web...{Colors.END}")
                resposta = bing.buscar_na_web(pergunta)
            else:
                resposta = resposta_gemini
        
        print(f"{Colors.CYAN}{resposta}{Colors.END}")
        
        if "Erro" not in resposta:
            historico_conversa.append(f"Usuário: {pergunta}")
            historico_conversa.append(f"Assistente: {resposta}")
            # Salva o histórico após cada interação
            historico.salvar_conversa(historico_conversa)
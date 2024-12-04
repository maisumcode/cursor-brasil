# Cores ANSI básicas para formatação de texto no terminal
class Colors:
    # Cores básicas
    BLUE = '\033[94m'      # Azul para títulos principais
    GREEN = '\033[32m'     # Verde mais suave para cabeçalhos de tabela
    CYAN = '\033[96m'      # Ciano para respostas gerais
    GRAY = '\033[90m'      # Cinza para separadores e informações secundárias
    BLACK = '\033[38;5;240m'  # Cinza escuro (mais suave que preto puro) para labels
    
    # Cores de destaque
    YELLOW = '\033[33m'    # Amarelo para avisos
    RED = '\033[91m'       # Vermelho brilhante para erros
    MAGENTA = '\033[35m'   # Magenta para informações especiais
    
    # Formatação
    BOLD = '\033[1m'       # Negrito
    UNDERLINE = '\033[4m'  # Sublinhado
    END = '\033[0m'        # Resetar formatação
    
    # Aliases semânticos
    WARNING = YELLOW
    FAIL = RED
    HEADER = MAGENTA
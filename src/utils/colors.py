# Cores ANSI básicas para formatação de texto no terminal
class Colors:
    # Reset
    END = '\033[0m'       # Reset all colors and styles
    
    # Regular Colors
    BLACK = '\033[0;30m'        # Black
    RED = '\033[0;31m'          # Red
    GREEN = '\033[0;32m'        # Green
    YELLOW = '\033[0;33m'       # Yellow
    BLUE = '\033[0;34m'         # Blue
    MAGENTA = '\033[0;35m'      # Magenta
    CYAN = '\033[0;36m'         # Cyan
    GRAY = '\033[0;37m'         # Gray
    
    # Bold
    BOLD = '\033[1m'               # Bold text
    BOLD_BLACK = '\033[1;30m'      # Bold Black
    BOLD_RED = '\033[1;31m'        # Bold Red
    BOLD_GREEN = '\033[1;32m'      # Bold Green
    BOLD_YELLOW = '\033[1;33m'     # Bold Yellow
    BOLD_BLUE = '\033[1;34m'       # Bold Blue
    BOLD_MAGENTA = '\033[1;35m'    # Bold Magenta
    BOLD_CYAN = '\033[1;36m'       # Bold Cyan
    BOLD_GRAY = '\033[1;37m'       # Bold Gray
    
    # Underline
    UNDERLINE = '\033[4m'          # Underline text
    
    # Background
    BG_BLACK = '\033[40m'          # Black Background
    BG_RED = '\033[41m'            # Red Background
    BG_GREEN = '\033[42m'          # Green Background
    BG_YELLOW = '\033[43m'         # Yellow Background
    BG_BLUE = '\033[44m'           # Blue Background
    BG_MAGENTA = '\033[45m'        # Magenta Background
    BG_CYAN = '\033[46m'           # Cyan Background
    BG_GRAY = '\033[47m'           # Gray Background
    
    # High Intensity
    BRIGHT_BLACK = '\033[0;90m'     # Bright Black
    BRIGHT_RED = '\033[0;91m'       # Bright Red
    BRIGHT_GREEN = '\033[0;92m'     # Bright Green
    BRIGHT_YELLOW = '\033[0;93m'    # Bright Yellow
    BRIGHT_BLUE = '\033[0;94m'      # Bright Blue
    BRIGHT_MAGENTA = '\033[0;95m'   # Bright Magenta
    BRIGHT_CYAN = '\033[0;96m'      # Bright Cyan
    BRIGHT_GRAY = '\033[0;97m'      # Bright Gray
    
    # Bold High Intensity
    BOLD_BRIGHT_BLACK = '\033[1;90m'    # Bold Bright Black
    BOLD_BRIGHT_RED = '\033[1;91m'      # Bold Bright Red
    BOLD_BRIGHT_GREEN = '\033[1;92m'    # Bold Bright Green
    BOLD_BRIGHT_YELLOW = '\033[1;93m'   # Bold Bright Yellow
    BOLD_BRIGHT_BLUE = '\033[1;94m'     # Bold Bright Blue
    BOLD_BRIGHT_MAGENTA = '\033[1;95m'  # Bold Bright Magenta
    BOLD_BRIGHT_CYAN = '\033[1;96m'     # Bold Bright Cyan
    BOLD_BRIGHT_GRAY = '\033[1;97m'     # Bold Bright Gray

    # Aliases semânticos
    WARNING = YELLOW
    FAIL = RED
    HEADER = MAGENTA
    SUCCESS = GREEN
    INFO = CYAN
    PROMPT = BRIGHT_GREEN
    RESPONSE = BRIGHT_CYAN
    SECONDARY = GRAY

    @classmethod
    def test_colors(cls):
        """Testa todas as cores disponíveis"""
        print("\nTeste de Cores Básicas:")
        print(f"{cls.BLACK}Texto Preto{cls.END}")
        print(f"{cls.RED}Texto Vermelho{cls.END}")
        print(f"{cls.GREEN}Texto Verde{cls.END}")
        print(f"{cls.YELLOW}Texto Amarelo{cls.END}")
        print(f"{cls.BLUE}Texto Azul{cls.END}")
        print(f"{cls.MAGENTA}Texto Magenta{cls.END}")
        print(f"{cls.CYAN}Texto Ciano{cls.END}")
        print(f"{cls.GRAY}Texto Cinza{cls.END}")
        
        print("\nTeste de Cores Brilhantes:")
        print(f"{cls.BRIGHT_BLACK}Texto Preto Brilhante{cls.END}")
        print(f"{cls.BRIGHT_RED}Texto Vermelho Brilhante{cls.END}")
        print(f"{cls.BRIGHT_GREEN}Texto Verde Brilhante{cls.END}")
        print(f"{cls.BRIGHT_YELLOW}Texto Amarelo Brilhante{cls.END}")
        print(f"{cls.BRIGHT_BLUE}Texto Azul Brilhante{cls.END}")
        print(f"{cls.BRIGHT_MAGENTA}Texto Magenta Brilhante{cls.END}")
        print(f"{cls.BRIGHT_CYAN}Texto Ciano Brilhante{cls.END}")
        print(f"{cls.BRIGHT_GRAY}Texto Cinza Brilhante{cls.END}")
        
        print("\nTeste de Estilos:")
        print(f"{cls.BOLD}Texto em Negrito{cls.END}")
        print(f"{cls.UNDERLINE}Texto Sublinhado{cls.END}")
        print(f"{cls.BOLD}{cls.UNDERLINE}Texto em Negrito e Sublinhado{cls.END}")
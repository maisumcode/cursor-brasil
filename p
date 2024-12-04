#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Obtém o diretório do script
script_dir = Path(__file__).parent.resolve()

# Adiciona o diretório do script ao PYTHONPATH
sys.path.append(str(script_dir))

# Importa e executa o script principal
from p import main

if __name__ == "__main__":
    main() 
#!/bin/bash

# Navega até o diretório onde está o script (ajuste o caminho conforme necessário)
cd "$(dirname "$0")"

# Ativa o ambiente virtual se estiver usando um
source .venv/bin/activate  

# Executa o script Python
python p.py 
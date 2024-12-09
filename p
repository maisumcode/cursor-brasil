#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log com cores
log() {
    local level=$1
    local msg=$2
    case $level in
        "info")  echo -e "${BLUE}[INFO]${NC} $msg" ;;
        "error") echo -e "${RED}[ERROR]${NC} $msg" ;;
        "success") echo -e "${GREEN}[OK]${NC} $msg" ;;
    esac
}

# Função para verificar dependências
check_deps() {
    command -v python3 >/dev/null 2>&1 || { log "error" "Python3 não encontrado"; exit 1; }
    command -v pip3 >/dev/null 2>&1 || { log "error" "Pip3 não encontrado"; exit 1; }
}

# Função para atualizar dependências
update_deps() {
    if [ -f "requirements.txt" ]; then
        log "info" "Verificando dependências..."
        pip install -r requirements.txt >/dev/null 2>&1
        log "success" "Dependências atualizadas"
    fi
}

# Caminho absoluto para o diretório do projeto
PROJECT_DIR="/Users/flow/Desktop/Desktop/cursor-brasil"

# Verifica dependências básicas
check_deps

# Navega até o diretório do projeto
cd "$PROJECT_DIR" || { log "error" "Erro ao acessar o diretório do projeto"; exit 1; }
log "success" "Diretório do projeto acessado"

# Verifica e cria ambiente virtual se necessário
if [ ! -d ".venv" ]; then
    log "info" "Criando ambiente virtual..."
    python3 -m venv .venv || { log "error" "Erro ao criar ambiente virtual"; exit 1; }
    log "success" "Ambiente virtual criado"
fi

# Ativa o ambiente virtual
source .venv/bin/activate || { log "error" "Erro ao ativar ambiente virtual"; exit 1; }
log "success" "Ambiente virtual ativado"

# Atualiza dependências se necessário
update_deps

# Executa o script Python
log "info" "Iniciando chat..."
python run.py

# Desativa o ambiente virtual ao sair
deactivate 2>/dev/null
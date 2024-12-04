# Assistente de Chat Inteligente

Sistema de chat interativo que utiliza múltiplas APIs para fornecer respostas precisas e atualizadas.

## Requisitos

- Python 3.x
- Pacotes Python listados em `requirements.txt`

## Configuração

1. Instale as dependências:

```bash
git clone https://github.com/seu-usuario/cursor-brasil.git
cd cursor-brasil
```

### 2. Configure o Ambiente Virtual

```bash
# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# No macOS/Linux:
source .venv/bin/activate
# No Windows:
.venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione suas chaves:

```
GEMINI_API_KEY=sua_chave_gemini
BING_SEARCH_V7_SUBSCRIPTION_KEY=sua_chave_bing
BING_SEARCH_V7_ENDPOINT=https://api.bing.microsoft.com
```

### 4. Torne o Script Executável

```bash
chmod +x p
```

### 5. Configure o Comando Global

#### No macOS/Linux:

```bash
# Crie um link simbólico para /usr/local/bin
sudo ln -s "$(pwd)/p" /usr/local/bin/p

# Se o diretório não existir, crie-o primeiro:
sudo mkdir -p /usr/local/bin
sudo chown $(whoami):admin /usr/local/bin
```

#### No Windows:

Adicione o diretório do projeto ao PATH do sistema.

## Como Usar

Depois de configurado, você pode usar o comando `p` de qualquer lugar no terminal:

```bash
p
```

### Comandos Disponíveis:

- Digite sua pergunta após o prompt ">"
- Digite "s" ou "sair" para encerrar o programa
- O programa responderá suas perguntas em português

### Funcionalidades

- Consulta ao Gemini para respostas inteligentes
- Busca automática na web via Bing Search quando:
  - O Gemini retorna erro
  - O Gemini indica não ter acesso à informação
  - O Gemini não pode fornecer a informação
- Consulta de preços de Bitcoin
- Formatação colorida das respostas
- Consulta de data e hora atual

### Requisitos

- Python 3.x
- Bibliotecas: requests, python-dotenv, beautifulsoup4
- Chave API do Google Gemini
- Chave API do Bing Search

## Desenvolvimento

### PR para mudanças

Por favor, abra Pull Requests para sugerir ajustes!

### Documentação Local

Instale o [Mintlify CLI](https://www.npmjs.com/package/mintlify) para visualizar as mudanças na documentação localmente:

```bash
npm i -g mintlify
```

Execute na raiz da documentação:

```bash
mintlify dev
```

#### Solução de Problemas

- Mintlify dev não está rodando - Execute `mintlify install`
- A página carrega como 404 - Verifique se está na pasta com `mint.json`

### Funcionalidades Especiais

- **Consultas de Data/Hora**: Perguntas como "que horas são" ou "data atual"
- **Preços de Bitcoin**: Consultas sobre preço atual do Bitcoin em BRL e USD
- **Histórico de Conversa**: Mantém as últimas 5 mensagens para contexto
- **Formatação Inteligente**: Respostas formatadas com cores para melhor legibilidade

### Variáveis de Ambiente Necessárias

```env
GEMINI_API_KEY=sua_chave_gemini          # Chave API do Google Gemini
BING_SEARCH_V7_SUBSCRIPTION_KEY=sua_chave # Chave API do Bing Search
BING_SEARCH_V7_ENDPOINT=endpoint_bing     # Endpoint do Bing Search (ex: https://api.bing.microsoft.com)
```

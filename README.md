# Documentação para Programar Mini apps usando IA

Este repositório contém o código-fonte para a [Documentação do Cursor](https://docs.cursor.com) e também inclui um mini aplicativo de chat usando a API do Google Gemini.

## Mini Chat com Gemini AI (Pesquisador)

### Sobre o Chat

O projeto inclui um chat interativo em português usando a API do Gemini para pesquisar informações. O nome do arquivo "p" vem de "pesquisar", pois este é um assistente focado em ajudar com pesquisas e consultas em português.

Para usar:

1. Certifique-se de ter o Python instalado no seu computador

2. Configure o arquivo `.env` com sua chave API do Gemini:

```
GEMINI_API_KEY="sua-chave-api-aqui"
```

3. Execute o pesquisador usando:

```bash
./p
```

4. Digite suas perguntas e receba respostas em português. Digite "sair" para encerrar.

### Requisitos

- Python 3.x (necessário ter instalado)
- Bibliotecas: requests, python-dotenv
- Chave API do Google Gemini

### Instalação

```bash
pip install requests python-dotenv
chmod +x p
```

## Documentação do Cursor

Por favor, abra Pull Requests para sugerir mudanças úteis!

### Desenvolvimento

Instale o [Mintlify CLI](https://www.npmjs.com/package/mintlify) para visualizar as mudanças na documentação localmente. Para instalar, use o seguinte comando:

```
npm i -g mintlify
```

Execute o seguinte comando na raiz da sua documentação (onde está o mint.json):

```
mintlify dev
```

#### Solução de Problemas

- Mintlify dev não está rodando - Execute `mintlify install` para reinstalar as dependências.
- A página carrega como 404 - Certifique-se de que você está executando em uma pasta com `mint.json`

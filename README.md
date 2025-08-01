# Telegram GenAI Bot

Um bot simples do Telegram que utiliza inteligência artificial generativa para responder mensagens.

## Funcionalidades

- 🤖 Respostas geradas por IA usando GPT-4o-mini
- 💬 Interface simples via Telegram
- 🧹 Comando para limpar histórico de conversa
- 📝 Comandos de ajuda integrados

## Configuração

### Pré-requisitos

- Python 3.8+
- Conta no Telegram
- Chave da API OpenAI

### Instalação

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd telegram-genai-bot-demo
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```
TELEGRAM_BOT_TOKEN=seu_token_do_bot
OPENAI_API_KEY=sua_chave_openai
```

### Como obter as credenciais

1. **Telegram Bot Token**:

   - Fale com @BotFather no Telegram
   - Use o comando `/newbot`
   - Siga as instruções para criar seu bot

2. **OpenAI API Key**:
   - Acesse [OpenAI Platform](https://platform.openai.com/)
   - Crie uma conta e gere uma chave de API

## Uso

Execute o bot:

```bash
python main.py
```

### Comandos disponíveis

- `/start` - Mensagem de boas-vindas
- `/help` - Mostra ajuda e comandos disponíveis
- `/clear_history` - Limpa o histórico da conversa

## Estrutura do Projeto

```
telegram-genai-bot-demo/
├── main.py              # Arquivo principal do bot
├── generative_service.py # Serviço de IA generativa
├── message_history.py   # Gerenciamento de histórico
├── environment.yaml     # Dependências do projeto
└── README.md           # Este arquivo
```

## Tecnologias Utilizadas

- **aiogram** - Framework para bots do Telegram
- **OpenAI** - API de inteligência artificial
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

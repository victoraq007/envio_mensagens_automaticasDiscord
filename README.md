# Bot Avisos Discord

![Bot Avatar](https://img.icons8.com/color/96/000000/discord-logo.png)

**Bot Avisos Discord** é um bot automatizado desenvolvido para gerenciar e enviar mensagens programadas em servidores Discord. Ele integra-se com o Google Sheets para gerenciar avisos e utiliza um sistema de logging robusto para monitorar suas operações, facilitando a manutenção e depuração.

## 🛠️ **Recursos**

- **Mensagens Semanais:** Envia mensagens semanais em horários definidos.
- **Mensagens Quinzenais:** Envia mensagens quinzenais com rotação de conteúdo.
- **Mensagens de Boas Tardes:** Envia mensagens de boas tardes a cada 15 minutos.
- **Lembretes de Ajuste de Ponto:** Envia lembretes em horários e dias específicos.
- **Mensagens de Realocação de Ticket:** Envia lembretes para realocação de tickets diariamente às 09:00.
- **Mensagens Oracle de Configuração:** Envia mensagens mensais relacionadas à configuração Oracle.
- **Integração com Google Sheets:** Envia avisos baseados em registros no Google Sheets.
- **Sistema de Logging:** Logs organizados para monitorar e depurar cada task individualmente.

## 📋 **Tabela de Conteúdos**

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
  - [Configuração do Discord Bot](#configuração-do-discord-bot)
  - [Configuração do Google Sheets](#configuração-do-google-sheets)
  - [Configuração do Arquivo `config.py`](#configuração-do-arquivo-configpy)
  - [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
- [🚀 Uso](#uso)
- [📝 Sistema de Logging](#sistema-de-logging)
- [📜 Comandos Disponíveis](#comandos-disponíveis)
- [🛠️ Contribuição](#contribuição)
- [📄 Licença](#licença)
- [📬 Contato](#contato)

## 🔍 **Pré-requisitos**

Antes de iniciar, certifique-se de ter o seguinte instalado:

- **Python 3.8 ou superior**
- **Pip** (gerenciador de pacotes Python)
- **Conta Discord** com permissões para adicionar bots a servidores
- **Google Cloud Account** para configurar as credenciais do Google Sheets

## 📥 **Instalação**

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/seu-usuario/bot-avisos-discord.git
   cd bot-avisos-discord


---

## 🛠️ Configuração

### 1. Configuração do Discord Bot

#### Criação do Bot
1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
2. Clique em **"New Application"** e dê um nome ao seu bot.
3. Navegue até a aba **"Bot"** e clique em **"Add Bot"**.
4. Copie o **Token** do bot e guarde-o em segurança.

#### Configurar Intents
1. Na aba **"Bot"**, habilite os seguintes intents:
   - **Presence Intent** (se necessário).
   - **Server Members Intent** (se necessário).
   - **Message Content Intent**.
   
#### Adicionar o Bot ao Servidor
1. Vá para a aba **"OAuth2"** > **"URL Generator"**.
2. Selecione o escopo **"bot"**.
3. Em **"Bot Permissions"**, selecione permissões como:
   - **Send Messages**.
   - **View Channels**.
4. Copie o link gerado e abra-o no navegador para adicionar o bot ao seu servidor.

---

### 2. Configuração do Google Sheets

#### Criar um Projeto no Google Cloud
1. Acesse o [Google Cloud Console](https://console.cloud.google.com).
2. Crie um novo projeto.
3. Ative as **APIs do Google Sheets** e **Google Drive**.

#### Criar Credenciais de Serviço
1. No **Google Cloud Console**, vá para **"APIs & Services"** > **"Credentials"**.
2. Clique em **"Create Credentials"** > **"Service Account"**.
3. Siga os passos para criar uma conta de serviço.
4. Após criar, vá para a conta de serviço e clique em:
   - **"Keys"** > **"Add Key"** > **"Create New Key"** > **"JSON"**.
5. Salve o arquivo JSON gerado.

#### Compartilhar a Planilha com a Conta de Serviço
1. Abra a planilha no Google Sheets.
2. Clique em **"Share"**.
3. Adicione o email da conta de serviço com permissões de **Editor**.

---

### 3. Configuração do Arquivo `config.py`

Crie o arquivo `config.py` na raiz do projeto com as seguintes variáveis:

python
# config.py
import pytz

# Token do Bot
TOKEN = "SEU_TOKEN_AQUI"

# IDs dos Canais
GOOD_AFTERNOON_CHANNEL_ID = 123456789012345678
AVISOS_GERAIS_CANAL = 123456789012345678

# Mensagens
SEMANAL_MESSAGES = ["Mensagem semanal 1", "Mensagem semanal 2"]
QUINZENAL_MESSAGES = ["Mensagem quinzenal 1", "Mensagem quinzenal 2"]

# Configurações do Google Sheets
GOOGLE_SHEETS_CREDENTIALS = "path/to/credentials.json"
GOOGLE_SHEETS_SPREADSHEET = "Nome da Planilha"
GOOGLE_SHEETS_WORKSHEET = "Nome da Worksheet"

# Fuso Horário
TIMEZONE = pytz.timezone('America/Sao_Paulo')

```
---

### 4. Configuração do Banco de Dados

#### Instale o SQLAlchemy
```bash
pip install sqlalchemy


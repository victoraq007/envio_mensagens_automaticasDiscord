# 🤖 **Bot Avisos Discord**

![Bot Avatar](https://img.icons8.com/color/96/000000/discord-logo.png)

**Bot Avisos Discord** é um bot automatizado desenvolvido para gerenciar e enviar mensagens programadas em servidores Discord. Com diversas funcionalidades integradas, ele facilita a comunicação e a organização dentro do seu servidor, permitindo a programação de mensagens semanais, quinzenais, diárias e muito mais.

## 🛠️ **Recursos**

- **Mensagens Semanais:** Envia mensagens semanais em horários definidos.
- **Mensagens Quinzenais:** Envia mensagens quinzenais com rotação de conteúdo.
- **Mensagens de Boas Tardes:** Envia mensagens de boas tardes a cada 15 minutos.
- **Lembretes de Ajuste de Ponto:** Envia lembretes em horários e dias específicos.
- **Mensagens de Realocação de Ticket:** Envia lembretes para realocação de tickets diariamente às 09:00.
- **Mensagens Oracle de Configuração:** Envia mensagens mensais relacionadas à configuração Oracle.
- **Mensagens CAHAMADA:** Envia mensagens aleatórias a cada 10 dias no canal `retail_noite` entre 15h e 23h.
- **Integração com Google Sheets:** Envia avisos baseados em registros no Google Sheets.
- **Sistema de Logging:** Logs organizados para monitorar e depurar cada task individualmente.
- **Comandos de Administração:** Facilita a gestão do bot através de comandos específicos.

## 📋 **Tabela de Conteúdos**

- [🔍 Pré-requisitos](#pré-requisitos)
- [📥 Instalação](#instalação)
- [📦 Configuração](#configuração)
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
- **Conta no Google Cloud** para configurar as credenciais do Google Sheets

## 📥 **Instalação**

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/seu-usuario/bot-avisos-discord.git
   cd bot-avisos-discord

   . **Crie um Ambiente Virtual (Recomendado)**
    
    ```bash

    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    
    ```
    
2. **Instale as Dependências**
    
    ```bash
    pip install -r requirements.txt
    ```
    
    **Conteúdo do `requirements.txt`:**
    
    ```
    discord.py
    gspread
    google-auth
    pytz
    SQLAlchemy
    python-dotenv
    
    ```
    

## 📦 **Configuração**

1. **Renomeie o Arquivo de Exemplo**
    
    ```bash
    cp config.py.example config.py
    
    ```
    
2. **Edite o `config.py` com Suas Informações**
    - Substitua `SEU_TOKEN_AQUI` pelo token do seu bot Discord.
    - Atualize os IDs dos canais com os IDs reais do seu servidor Discord.
    - Configure as mensagens conforme desejar.
    - Configure as credenciais do Google Sheets.

### 🔧 **Configuração do Discord Bot**

- **Crie um Bot no Discord Developer Portal:**
    1. Acesse Discord Developer Portal.
    2. Clique em **"New Application"** e dê um nome ao seu bot.
    3. Navegue até a aba **"Bot"** e clique em **"Add Bot"**.
    4. Copie o **Token** do bot. **Mantenha-o seguro!**
- **Configurar Intents:**
    - No Developer Portal, na aba **"Bot"**, habilite os intents necessários:
        - **Presence Intent** (se necessário)
        - **Server Members Intent** (se necessário)
        - **Message Content Intent**
- **Adicionar o Bot ao Servidor:**
    1. No Developer Portal, vá para a aba **"OAuth2"** > **"URL Generator"**.
    2. Selecione **"bot"** nos escopos.
    3. Em **"Bot Permissions"**, selecione as permissões necessárias, como **"Send Messages"**, **"View Channels"**, etc.
    4. Copie o link gerado e abra no navegador para adicionar o bot ao seu servidor Discord.

### 🔧 **Configuração do Google Sheets**

- **Criar um Projeto no Google Cloud:**
    1. Acesse Google Cloud Console.
    2. Crie um novo projeto.
    3. Ative a API do **Google Sheets** e **Google Drive** para o projeto.
- **Criar Credenciais de Serviço:**
    1. No Google Cloud Console, navegue até **"APIs & Services"** > **"Credentials"**.
    2. Clique em **"Create Credentials"** > **"Service Account"**.
    3. Siga os passos para criar uma conta de serviço.
    4. Após criar, vá para a conta de serviço e clique em **"Keys"** > **"Add Key"** > **"Create New Key"** > **"JSON"**. Salve o arquivo JSON.
- **Compartilhar a Planilha com a Conta de Serviço:**
    1. Abra a planilha no Google Sheets.
    2. Clique em **"Share"** e adicione o email da conta de serviço com permissões de **"Editor"**.

### 🔧 **Configuração do Arquivo `config.py`**

Atualize o `config.py` com todas as informações necessárias. Um exemplo de `config.py.example` está disponível para referência.

```python
# config.py.example

import pytz

TOKEN = "SEU_TOKEN_AQUI"

# IDs dos canais (Substitua pelos IDs reais)
GOOD_AFTERNOON_CHANNEL_ID = 123456789012345678  # Canal de boas tardes
AVISOS_GERAIS_CANAL = 123456789012345678       # Canal de avisos gerais
RETAIL_NOITE_CHANNEL_ID = 987654321098765432  # Canal retail_noite

# Mensagens e Configurações
SEMANAL_MESSAGES = [
    "Mensagem semanal 1",
    "Mensagem semanal 2",
    # Adicione mais mensagens conforme necessário
]

QUINZENAL_MESSAGES = [
    "Mensagem quinzenal 1",
    "Mensagem quinzenal 2",
    # Adicione mais mensagens conforme necessário
]

MENSAGENS_ALERTA_PONTO = [
    "Lembrete para ajustar ponto 1",
    "Lembrete para ajustar ponto 2",
    # Adicione mais mensagens conforme necessário
]

MENSAGENS_ALERTA_REALOCACAO = [
    "Lembrete de realocação de ticket 1",
    "Lembrete de realocação de ticket 2",
    # Adicione mais mensagens conforme necessário
]

MENSAGENS_ALERTA_ORACLE_CONFIGURACAO = [
    "Mensagem Oracle 1",
    "Mensagem Oracle 2",
    # Adicione mais mensagens conforme necessário
]

CAHAMADA_MESSAGES = [
    "🐾 Descubra uma curiosidade fascinante sobre a natureza hoje!",
    "🦁 Sabia que os leões podem dormir até 20 horas por dia?",
    "🐧 Os pinguins têm joelhos! Interessante, não é?",
    "🦉 As corujas podem girar suas cabeças até 270 graus.",
    "🐘 Elefantes são os únicos animais que não conseguem pular.",
    # Adicione mais mensagens conforme necessário
]

TIMEZONE = pytz.timezone('America/Sao_Paulo')  # Substitua pelo seu fuso horário

# Configurações do Google Sheets
GOOGLE_SHEETS_CREDENTIALS = "path/to/credentials.json"  # Caminho para o arquivo JSON das credenciais
GOOGLE_SHEETS_SPREADSHEET = "Nome da Planilha"         # Nome da planilha no Google Sheets
GOOGLE_SHEETS_WORKSHEET = "Nome da Worksheet"         # Nome da worksheet dentro da planilha

# Outros IDs e configurações
CHANNEL_IDS = [
    123456789012345678,  # Substitua com os IDs dos canais quinzenais
    # Adicione mais IDs conforme necessário
]

REALOCACAO_CANAL = 123456789012345678  # ID do canal de realocação de ticket

DEBUG = True  # Defina como True para modo de teste, False para produção

```

### 🔧 **Configuração do Banco de Dados**

O bot utiliza um banco de dados para armazenar configurações como a última data em que uma mensagem foi enviada.

1. **Instale o SQLAlchemy:**
    
    ```bash
    pip install sqlalchemy
    ```
    
2. **Crie os Arquivos de Configuração:**
    
    **`models.py`:**
    
    ```python
    # models.py
    
    from sqlalchemy import Column, String, Integer
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    
    class Settings(Base):
        __tablename__ = 'settings'
    
        id = Column(Integer, primary_key=True, autoincrement=True)
        key = Column(String, unique=True, nullable=False)
        value = Column(String, nullable=False)
    
    ```
    
    **`database.py`:**
    
    ```python
    # database.py
    
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models import Base
    
    DATABASE_URL = "sqlite:///bot_database.db"  # Use o banco de dados de sua preferência
    
    engine = create_engine(DATABASE_URL, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Crie as tabelas no banco de dados
    Base.metadata.create_all(engine)
    
    ```
    

## 🚀 **Uso**

1. **Inicie o Bot**
    
    ```bash
    python main.py
    
    ```
    
2. **Verifique a Inicialização**
    - No terminal, você verá a mensagem: `Bot conectado como NomeDoBot`.
    - Os arquivos de log serão criados na pasta `logs/`.
3. **Comandos de Teste (Opcional)**
    
    Utilize comandos como `!listar_canais` e `!teste_cahamada` para verificar funcionalidades específicas.
    

## 📝 **Sistema de Logging**

O bot utiliza um sistema de logging robusto para monitorar suas operações. Cada task possui seu próprio arquivo de log, facilitando a identificação e depuração de problemas específicos.

### **Estrutura dos Logs**

```c
logs/
├── geral.log
├── erros.log
├── task_semanal.log
├── task_good_afternoon.log
├── ajustar_ponto.log
├── quinzenal_message.log
├── enviar_realocacao_ticket.log
├── oracle_configuracao.log
├── enviar_aviso_excel.log
└── cahamada.log  # Novo arquivo de log

```

### **Rotação de Logs**

Os logs utilizam `RotatingFileHandler` para evitar que os arquivos cresçam indefinidamente. Cada arquivo de log tem um tamanho máximo de 5MB com até 5 backups.

## 📜 **Comandos Disponíveis**

### **Listar Canais**

- **Comando:** `!listar_canais`
- **Descrição:** Lista todos os canais que o bot pode acessar no servidor.
- **Uso:**
    - No Discord, digite `!listar_canais` em qualquer canal onde o bot tenha acesso.
    - O bot responderá com uma lista de canais, incluindo o nome da guilda, ID do canal e nome do canal.

**Exemplo:**

```
!listar_canais

```

**Resposta:**

```
Canais que o bot pode acessar:
Guilda: NomeDaGuilda | ID: 123456789012345678 | Nome: geral
Guilda: NomeDaGuilda | ID: 234567890123456789 | Nome: boas-tardes
...

```

**Nota:** Este comando é útil para verificar se o ID do canal está correto e acessível pelo bot.

### **Comando de Teste: `!teste_cahamada`**

- **Comando:** `!teste_cahamada`
- **Descrição:** Envia uma mensagem aleatória da lista **CAHAMADA** no canal `retail_noite`.
- **Uso:**
    - No Discord, digite `!teste_cahamada` em qualquer canal onde o bot tenha acesso.
    - O bot responderá com uma mensagem aleatória no canal `retail_noite`.

**Exemplo:**

```
!teste_cahamada

```

**Resposta:**

```
Mensagem de teste CAHAMADA enviada com sucesso!
```

## 🛠️ **Contribuição**

Contribuições são bem-vindas! Se você encontrar algum problema ou desejar adicionar novos recursos, siga os passos abaixo:

1. **Fork o Repositório**
2. **Crie uma Branch para sua Feature ou Fix**
    
    ```bash
    git checkout -b feature/nova-feature
    
    ```
    
3. **Commit suas Alterações**
    
    ```bash
    git commit -m "Adiciona nova feature"
    ```
    
4. **Push para a Branch**
    
    ```bash
    git push origin feature/nova-feature
    ```
    
5. **Abra um Pull Request**

Leia o arquivo `CONTRIBUTING.md` para mais detalhes sobre o processo de contribuição.

## 📄 **Licença**

Este projeto está licenciado sob a MIT License.

## 📬 **Contato**

Se você tiver dúvidas ou sugestões, sinta-se à vontade para entrar em contato:

- **Email:** victoraquinoribeiro@gmail.com
- **GitHub:** [victor007](https://github.com/victoraq007)
-

---

**Agradecemos por utilizar o Bot Avisos Discord!**

Desenvolvido com ❤️ por [Victor Aquino ](https://github.com/victoraq007)

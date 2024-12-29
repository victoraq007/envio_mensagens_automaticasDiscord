# main.py

import discord
from discord.ext import commands
from config import TOKEN
from cogs.tasks_cog import TasksCog
import os
import logging
from logging.handlers import RotatingFileHandler

# Garantir que a pasta 'logs' existe
os.makedirs('logs', exist_ok=True)

# Configuração do Logger Geral
geral_logger = logging.getLogger("discord_bot")
geral_logger.setLevel(logging.DEBUG)  # Captura todos os níveis de log

# Formato do Log
formatter = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Handler para Log Geral (INFO e superiores)
geral_log_path = os.path.join('logs', 'geral.log')
geral_handler = RotatingFileHandler(
    filename=geral_log_path,
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=5,
    encoding='utf-8'
)
geral_handler.setLevel(logging.INFO)
geral_handler.setFormatter(formatter)
geral_logger.addHandler(geral_handler)

# Handler para Logs de Erro (ERROR e superiores)
erros_log_path = os.path.join('logs', 'erros.log')
erros_handler = RotatingFileHandler(
    filename=erros_log_path,
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=5,
    encoding='utf-8'
)
erros_handler.setLevel(logging.ERROR)
erros_handler.setFormatter(formatter)
geral_logger.addHandler(erros_handler)

# Configuração do Logger da Biblioteca discord.py
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.WARNING)  # Suprimindo logs muito verbosos

# Criação do Bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """
    Este evento é chamado apenas uma vez, quando o bot se conecta com sucesso ao Discord.
    """
    geral_logger.info(f"Bot conectado como {bot.user}")
    print(f"INICIALIZACAO DO BOT (MAIN) ----- {bot.user}")

def main():
    # Adiciona o Cog com as tarefas, passando o logger geral
    bot.add_cog(TasksCog(bot, geral_logger))
    
    # Executa o bot
    bot.run(TOKEN)

if __name__ == "__main__":
    main()

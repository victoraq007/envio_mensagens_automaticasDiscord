# config.py.example

import pytz
import os

DEBUG = True  # Defina como True para modo de teste, False para produção
TIMEZONE = pytz.timezone('America/Sao_Paulo')  # Substitua pelo seu fuso horário

# Configurações do Google Sheets
GOOGLE_SHEETS_CREDENTIALS = "path/to/credentials.json"  # Caminho para o arquivo JSON das credenciais
GOOGLE_SHEETS_SPREADSHEET = "Nome da Planilha"         # Nome da planilha no Google Sheets
GOOGLE_SHEETS_WORKSHEET = "Nome da Worksheet"         # Nome da worksheet dentro da planilha


TOKEN = "SEU_TOKEN_AQUI" ## Token discord

# IDs dos canais (Substitua pelos IDs reais)
GOOD_AFTERNOON_CHANNEL_ID = 123456789012345678  # Canal de boas tardes
AVISOS_GERAIS_CANAL = 123456789012345678       # Canal de avisos gerais
CANAL_DOIS_ID = 123456789012345678  # Canal exemplo dois


# Outros IDs e configurações
CHANNEL_IDS = [
    123456789012345678,  # Substitua com os IDs dos canais quinzenais
    # Adicione mais IDs conforme necessário , podendo então agrupar varios canais de uma vez só
]

REALOCACAO_CANAL = 123456789012345678  # ID do canal de realocação de ticket


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


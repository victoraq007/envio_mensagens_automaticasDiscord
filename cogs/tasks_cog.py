# cogs/tasks_cog.py

import os
from google.oauth2.service_account import Credentials
import random
import datetime
import gspread
from discord.ext import tasks, commands
from config import (
    CHANNEL_IDS,
    GOOD_AFTERNOON_CHANNEL_ID,
    TIMEZONE,
    QUINZENAL_MESSAGES,
    SEMANAL_MESSAGES,
    AVISOS_GERAIS_CANAL,
    MENSAGENS_ALERTA_PONTO,
    REALOCACAO_CANAL,
    MENSAGENS_ALERTA_REALOCACAO,
    MENSAGENS_ALERTA_ORACLE_CONFIGURACAO,
    GOOGLE_SHEETS_CREDENTIALS,
    GOOGLE_SHEETS_SPREADSHEET,
    GOOGLE_SHEETS_WORKSHEET,
    CANAL_DOIS_ID,
    CAHAMADA_MESSAGES,
    DEBUG,
)
import asyncio
from database import session
from models import Settings
import logging


# Função auxiliar para retornar a data/hora no fuso definido.
def get_now():
    return datetime.datetime.now(TIMEZONE)


# Função para conectar ao Google Sheets (em stand by)
def conectar_google_sheets():
    """Conecta-se ao Google Sheets e retorna a worksheet especificada."""
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(
            GOOGLE_SHEETS_CREDENTIALS, scopes=scopes
        )
        client = gspread.authorize(creds)
        sheet = client.open(GOOGLE_SHEETS_SPREADSHEET)
        worksheet = sheet.worksheet(GOOGLE_SHEETS_WORKSHEET)
        return worksheet
    except Exception as e:
        # O log de erro será tratado pela task que chama esta função
        raise e


class TasksCog(commands.Cog):
    def __init__(self, bot: commands.Bot, geral_logger: logging.Logger):
        self.bot = bot
        self.geral_logger = geral_logger

        # Configuração dos loggers específicos para cada task
        self.task_semanal_logger = self.setup_logger(
            "discord_bot.task_semanal", "task_semanal.log"
        )
        self.task_good_afternoon_logger = self.setup_logger(
            "discord_bot.task_good_afternoon", "task_good_afternoon.log"
        )
        self.task_ajustar_ponto_logger = self.setup_logger(
            "discord_bot.task_ajustar_ponto", "ajustar_ponto.log"
        )
        self.task_quinzenal_logger = self.setup_logger(
            "discord_bot.task_quinzenal", "quinzenal_message.log"
        )
        self.task_enviar_realocacao_ticket_logger = self.setup_logger(
            "discord_bot.task_enviar_realocacao_ticket", "enviar_realocacao_ticket.log"
        )
        self.task_oracle_configuracao_logger = self.setup_logger(
            "discord_bot.task_oracle_configuracao", "oracle_configuracao.log"
        )
        self.task_enviar_aviso_excel_logger = self.setup_logger(
            "discord_bot.task_enviar_aviso_excel", "enviar_aviso_excel.log"
        )
        self.task_mundo_animal_logger = self.setup_logger(
            "discord_bot.task_mundo_animal", "mundo_animal.log"
        )

        # Iniciar as tasks (elas só rodam quando o bot está pronto).
        self.semanal_message_task.start()
        self.send_good_afternoon_message.start()
        self.ajustar_ponto_task.start()
        self.quinzenal_message_task.start()
        self.enviar_realocacao_ticket.start()
        self.oracle_configuracao_task.start()
        self.enviar_aviso_excel.start()
        self.mundo_animal_task.start()

    def setup_logger(self, logger_name: str, log_filename: str) -> logging.Logger:
        """
        Configura um logger específico para uma task.
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        log_file_path = os.path.join("logs", log_filename)
        handler = logging.FileHandler(
            filename=log_file_path, encoding="utf-8", mode="a"
        )
        formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    # =====================================================
    # Evento: quando o bot estiver pronto
    # =====================================================
    @commands.Cog.listener()
    async def on_ready(self):
        self.geral_logger.info(
            f"INICIALIZAÇÃO - Cog de Tasks carregado!Bot conectado como {self.bot.user}"
        )
        print(
            f"INICIALIZAÇÃO - Cog de Tasks carregado! Bot conectado como {self.bot.user}"
        )

    # =====================================================
    # Tarefa: Mensagem Semanal (uma vez por semana, qualquer dia entre 09:00 e 18:00)
    # =====================================================
    @tasks.loop(hours=1)  # Executa a task a cada hora
    async def semanal_message_task(self):
        try:
            now = get_now()
            current_week = now.isocalendar()[1]  # Número da semana atual

            # Recuperar a última semana enviada do banco de dados
            setting = session.query(Settings).filter_by(key="last_week_sent").first()
            last_week_sent = int(setting.value) if setting else None

            if current_week != last_week_sent:
                current_hour = now.hour

                # Verifica se está entre 09:00 e 18:00
                if 9 <= current_hour < 18:
                    # Seleciona uma mensagem aleatória da lista semanal
                    message = random.choice(SEMANAL_MESSAGES)

                    # Enviar a mensagem para o canal especificado
                    channel = self.bot.get_channel(AVISOS_GERAIS_CANAL)
                    if channel:
                        try:
                            await channel.send(message)
                            self.task_semanal_logger.info(
                                f"Mensagem semanal enviada no canal {AVISOS_GERAIS_CANAL} às {now.strftime('%H:%M:%S')}."
                            )
                            print(
                                f"[{now.strftime('%H:%M:%S')}] Enviada mensagem semanal no canal {AVISOS_GERAIS_CANAL}."
                            )

                            # Atualizar a semana enviada no banco de dados
                            if setting:
                                setting.value = str(current_week)
                            else:
                                new_setting = Settings(
                                    key="last_week_sent", value=str(current_week)
                                )
                                session.add(new_setting)
                            session.commit()
                        except Exception as e:
                            self.task_semanal_logger.exception(
                                f"Erro ao enviar mensagem semanal: {e}"
                            )
                            print(f"Erro ao enviar mensagem semanal: {e}")
                    else:
                        self.task_semanal_logger.error(
                            f"Canal com IDDDD {AVISOS_GERAIS_CANAL} não encontrado."
                        )
                        print(f"Canal com ID {AVISOS_GERAIS_CANAL} não encontrado.")
            else:
                self.task_semanal_logger.info(
                    "Mensagem semanal já foi enviada esta semana."
                )
                print("Mensagem semanal já foi enviada esta semana.")
        except Exception as e:
            self.task_semanal_logger.exception(
                f"Erro na task semanal_message_task: {e}"
            )

    @semanal_message_task.before_loop
    async def before_semanal_message_task(self):
        await self.bot.wait_until_ready()
        self.task_semanal_logger.info("Tarefa semanal_message_task iniciada.")
        print("Tarefa semanal_message_task iniciada.")

    ## listar canais no discord
    def listar_canais_acessiveis(self):
        """
        Lista todos os canais que o bot pode acessar na guilda.
        """
        canais = []
        for guild in self.bot.guilds:
            for channel in guild.channels:
                canais.append((guild.name, channel.id, channel.name))
        return canais

    @commands.command(name="listar_canais")
    async def listar_canais(self, ctx):
        """
        Comando para listar todos os canais que o bot pode acessar.
        """
        canais = self.listar_canais_acessiveis()
        mensagem = "Canais que o bot pode acessar:\n"
        for guild_name, channel_id, channel_name in canais:
            mensagem += (
                f"Guilda: {guild_name} | ID: {channel_id} | Nome: {channel_name}\n"
            )
        await ctx.send(mensagem)

    # =====================================================
    # Tarefa de 15 em 15 minutos
    # =====================================================
    @tasks.loop(minutes=15)
    async def send_good_afternoon_message(self):
        try:
            now = get_now()
            message = f"@everyone teste chat funcional food afternon de 15 em 15 minutos as  ({now.strftime('%Y-%m-%d %H:%M:%S')})"

            channel = self.bot.get_channel(GOOD_AFTERNOON_CHANNEL_ID)
            if channel:
                try:
                    await channel.send(message)
                    self.task_good_afternoon_logger.info(
                        f"[{now.strftime('%H:%M:%S')}] Mensagem de teste enviada no canal {GOOD_AFTERNOON_CHANNEL_ID}."
                    )
                except Exception as e:
                    self.task_good_afternoon_logger.exception(
                        f"Erro ao enviar mensagem de teste: {e}"
                    )
            else:
                self.task_good_afternoon_logger.error(
                    f"Canal com ID {GOOD_AFTERNOON_CHANNEL_ID} não encontrado."
                )
        except Exception as e:
            self.task_good_afternoon_logger.exception(
                f"Erro na task send_good_afternoon_message: {e}"
            )

    # =====================================================
    # Tarefa para enviar lembrete de ajustar ponto
    # =====================================================
    @tasks.loop(minutes=1)
    async def ajustar_ponto_task(self):
        try:
            now = get_now()
            # Verifica se é dia 16, 17, 18, 19, 20 ou 21 e se o horário é 10:10 ou 18:14
            if now.day in [16, 17, 18, 19, 20, 21] and now.strftime("%H:%M") in [
                "10:10",
                "18:14",
            ]:
                # Seleciona uma mensagem aleatória da lista
                message = random.choice(MENSAGENS_ALERTA_PONTO)

                # Obtém o canal específico
                channel = self.bot.get_channel(AVISOS_GERAIS_CANAL)
                if channel:
                    try:
                        await channel.send(message)
                        self.task_ajustar_ponto_logger.info(
                            f"[{now.strftime('%Y-%m-%d %H:%M')}] Alerta de ponto enviado no canal {AVISOS_GERAIS_CANAL}."
                        )
                        print(
                            f"[{now.strftime('%Y-%m-%d %H:%M')}] Alerta de ponto enviado no canal {AVISOS_GERAIS_CANAL}."
                        )
                    except Exception as e:
                        self.task_ajustar_ponto_logger.exception(
                            f"Erro ao enviar alerta de ponto: {e}"
                        )
                else:
                    self.task_ajustar_ponto_logger.error(
                        f"Canal com ID {AVISOS_GERAIS_CANAL} não encontrado."
                    )
        except Exception as e:
            self.task_ajustar_ponto_logger.exception(
                f"Erro na task ajustar_ponto_task: {e}"
            )

    # =====================================================
    # Tarefa para enviar mensagem quinzenalmente
    # =====================================================
    @tasks.loop(hours=24)
    async def quinzenal_message_task(self):
        try:
            now = get_now()
            # Dia divisível por 15 (ex.: dia 15, 30, etc.)
            if now.day % 15 == 0:
                for channel_id in CHANNEL_IDS:
                    channel = self.bot.get_channel(channel_id)
                    if channel:
                        try:
                            await channel.send(QUINZENAL_MESSAGES[self.quinzenal_index])
                            self.task_quinzenal_logger.info(
                                f"[{now.strftime('%H:%M:%S')}] Enviada mensagem quinzenal no canal {channel_id}"
                            )
                            print(
                                f"[{now.strftime('%H:%M:%S')}] Enviada mensagem quinzenal no canal {channel_id}"
                            )
                        except Exception as e:
                            self.task_quinzenal_logger.exception(
                                f"Erro ao enviar mensagem quinzenal no canal {channel_id}: {e}"
                            )
                # Atualiza o índice (rotação circular)
                self.quinzenal_index = (self.quinzenal_index + 1) % len(
                    QUINZENAL_MESSAGES
                )
        except Exception as e:
            self.task_quinzenal_logger.exception(
                f"Erro na task quinzenal_message_task: {e}"
            )

    @quinzenal_message_task.before_loop
    async def before_quinzenal_message_task(self):
        await self.bot.wait_until_ready()
        self.task_quinzenal_logger.info("Tarefa quinzenal_message_task iniciada.")
        print("Tarefa quinzenal_message_task iniciada.")

    # =====================================================
    # Tarefa para enviar lembrete de realocação de ticket
    # =====================================================
    @tasks.loop(minutes=1)
    async def enviar_realocacao_ticket(self):
        try:
            now = get_now()
            # Verifica se é 09:00 da manhã
            if now.strftime("%H:%M") == "09:00":
                # Seleciona uma mensagem aleatória da lista específica
                message = random.choice(MENSAGENS_ALERTA_REALOCACAO)

                # Enviar a mensagem no canal específico
                channel = self.bot.get_channel(
                    REALOCACAO_CANAL
                )  # Substitua pelo canal correto
                if channel:
                    try:
                        await channel.send(message)
                        self.task_enviar_realocacao_ticket_logger.info(
                            f"Mensagem de realocação enviada no canal {REALOCACAO_CANAL} às {now.strftime('%H:%M:%S')}."
                        )
                        print(
                            f"Mensagem de realocação enviada no canal {REALOCACAO_CANAL} às {now.strftime('%H:%M:%S')}."
                        )
                    except Exception as e:
                        self.task_enviar_realocacao_ticket_logger.exception(
                            f"Erro ao enviar mensagem de realocação no canal {REALOCACAO_CANAL}: {e}"
                        )
                else:
                    self.task_enviar_realocacao_ticket_logger.error(
                        f"Canal com ID {REALOCACAO_CANAL} não encontrado."
                    )
        except Exception as e:
            self.task_enviar_realocacao_ticket_logger.exception(
                f"Erro na task enviar_realocacao_ticket: {e}"
            )

    # =====================================================
    # Task: Enviar Mensagem Oracle Configuração (Mensal)
    # =====================================================
    @tasks.loop(hours=1)  # Executa a task a cada hora
    async def oracle_configuracao_task(self):
        try:
            now = get_now()
            current_month = now.month  # Mês atual

            # Recuperar o último mês enviado do banco de dados
            setting = (
                session.query(Settings).filter_by(key="last_month_oracle_sent").first()
            )
            last_month_sent = int(setting.value) if setting else None

            if current_month != last_month_sent:
                current_hour = now.hour
                # Verifica se está entre 09:00 e 18:00
                if 9 <= current_hour < 18:
                    # Seleciona uma mensagem aleatória da lista de configurações Oracle
                    message = random.choice(MENSAGENS_ALERTA_ORACLE_CONFIGURACAO)

                    # Enviar a mensagem para o canal especificado
                    channel = self.bot.get_channel(
                        AVISOS_GERAIS_CANAL
                    )  # Substitua pelo canal correto
                    if channel:
                        try:
                            await channel.send(message)
                            self.task_oracle_configuracao_logger.info(
                                f"Mensagem Oracle enviada no canal {AVISOS_GERAIS_CANAL} às {now.strftime('%H:%M:%S')}."
                            )
                            print(
                                f"[{now.strftime('%H:%M:%S')}] Enviada mensagem Oracle no canal {AVISOS_GERAIS_CANAL}."
                            )

                            # Atualizar o mês enviado no banco de dados
                            if setting:
                                setting.value = str(current_month)
                            else:
                                new_setting = Settings(
                                    key="last_month_oracle_sent",
                                    value=str(current_month),
                                )
                                session.add(new_setting)
                            session.commit()
                        except Exception as e:
                            self.task_oracle_configuracao_logger.exception(
                                f"Erro ao enviar mensagem Oracle: {e}"
                            )
                            print(f"Erro ao enviar mensagem Oracle: {e}")
                    else:
                        self.task_oracle_configuracao_logger.error(
                            f"Canal com ID {AVISOS_GERAIS_CANAL} não encontrado."
                        )
                        print(f"Canal com ID {AVISOS_GERAIS_CANAL} não encontrado.")
            else:
                self.task_oracle_configuracao_logger.info(
                    "Mensagem Oracle já foi enviada este mês."
                )
                print("Mensagem Oracle já foi enviada este mês.")
        except Exception as e:
            self.task_oracle_configuracao_logger.exception(
                f"Erro na task oracle_configuracao_task: {e}"
            )

    @oracle_configuracao_task.before_loop
    async def before_oracle_configuracao_task(self):
        await self.bot.wait_until_ready()
        self.task_oracle_configuracao_logger.info(
            "Tarefa oracle_configuracao_task iniciada."
        )
        print("Tarefa oracle_configuracao_task iniciada.")

    # =====================================================
    # Task: Enviar Aviso a partir do Google Sheets
    # =====================================================
    @tasks.loop(minutes=15)  # Temporariamente rodando a cada minuto para testes
    async def enviar_aviso_excel(self):
        try:
            self.task_enviar_aviso_excel_logger.info(
                "Iniciando a execução da task 'enviar_aviso_excel'."
            )
            worksheet = conectar_google_sheets()
            if worksheet is None:
                self.task_enviar_aviso_excel_logger.error(
                    "Não foi possível conectar ao Google Sheets."
                )
                return

            # Obter todas as linhas da planilha como dicionários
            registros = worksheet.get_all_records()
            self.task_enviar_aviso_excel_logger.info(
                f"Número de registros encontrados na planilha: {len(registros)}."
            )

            for registro in registros:
                self.task_enviar_aviso_excel_logger.debug(
                    f"Processando registro: {registro}"
                )
                # Verificar se o aviso já foi enviado
                enviado = registro.get("Enviado", "").strip().upper()
                self.task_enviar_aviso_excel_logger.debug(
                    f"Aviso ID {registro.get('ID')}: Enviado = {enviado}"
                )

                if enviado != "TRUE":
                    canal_id = registro.get("Canal_ID")
                    mensagem = registro.get("Mensagem")
                    data_envio_str = registro.get("Data")
                    id_aviso = registro.get("ID")

                    # Validar campos essenciais
                    if not (canal_id and mensagem and data_envio_str and id_aviso):
                        self.task_enviar_aviso_excel_logger.warning(
                            f"Aviso com ID {id_aviso} possui campos incompletos. Pulando."
                        )
                        continue

                    # Converter string de data para objeto date
                    try:
                        data_envio = datetime.datetime.strptime(
                            data_envio_str, "%Y-%m-%d"
                        ).date()
                    except ValueError as ve:
                        self.task_enviar_aviso_excel_logger.error(
                            f"Formato de data inválido para aviso ID {id_aviso}: {data_envio_str}. Pulando."
                        )
                        continue

                    hoje = datetime.datetime.now().date()
                    self.task_enviar_aviso_excel_logger.debug(
                        f"Aviso ID {id_aviso}: Data de envio = {data_envio} | Data atual = {hoje}"
                    )

                    # Verificar se a data de envio é hoje
                    if data_envio == hoje:
                        try:
                            canal = self.bot.get_channel(int(canal_id))
                            if canal:
                                await canal.send(mensagem)
                                self.task_enviar_aviso_excel_logger.info(
                                    f"Mensagem enviada para o canal {canal_id}: {mensagem}"
                                )
                                print(
                                    f"Mensagem enviada para o canal {canal_id}: {mensagem}"
                                )

                                # Atualizar a flag 'Enviado' na planilha
                                try:
                                    cell = worksheet.find(str(id_aviso))
                                    if cell:
                                        # Assumindo que a coluna 'Enviado' é a 5ª coluna (E)
                                        worksheet.update_cell(cell.row, 5, "TRUE")
                                        self.task_enviar_aviso_excel_logger.info(
                                            f"Aviso ID {id_aviso} marcado como enviado."
                                        )
                                    else:
                                        self.task_enviar_aviso_excel_logger.error(
                                            f"Aviso ID {id_aviso} não encontrado na planilha."
                                        )
                                except Exception as update_exc:
                                    self.task_enviar_aviso_excel_logger.exception(
                                        f"Erro ao atualizar a planilha para aviso ID {id_aviso}: {update_exc}"
                                    )
                            else:
                                self.task_enviar_aviso_excel_logger.error(
                                    f"Canal com ID {canal_id} não encontrado."
                                )
                                print(f"Canal com ID {canal_id} não encontrado.")
                        except Exception as send_exc:
                            self.task_enviar_aviso_excel_logger.exception(
                                f"Erro ao enviar mensagem para o canal {canal_id}: {send_exc}"
                            )
        except Exception as e:
            self.task_enviar_aviso_excel_logger.exception(
                f"Erro na task enviar_aviso_excel: {e}"
            )
            print(f"Erro na task enviar_aviso_excel: {e}")

    @enviar_aviso_excel.before_loop
    async def before_enviar_aviso_excel(self):
        await self.bot.wait_until_ready()
        self.task_enviar_aviso_excel_logger.info("Tarefa enviar_aviso_excel iniciada.")
        print("Tarefa enviar_aviso_excel iniciada.")

    # =====================================================
    # Task: MUNDO ANIMAL (Enviar mensagem a cada 10 dias)
    # =====================================================
    @tasks.loop(hours=24)  # Executa a task diariamente
    async def mundo_animal_task(self):
        try:
            now = self.get_now()
            today = now.date()

            # Recuperar a última data de envio do banco de dados
            setting = (
                session.query(Settings).filter_by(key="last_mundo_animal_sent").first()
            )
            last_sent_date = (
                datetime.datetime.strptime(setting.value, "%Y-%m-%d").date()
                if setting
                else None
            )

            if setting:
                days_since_last = (today - last_sent_date).days
            else:
                days_since_last = 10  # Força o envio na primeira execução

            # Definir o intervalo de dias com base na flag DEBUG
            required_days = 10 if not DEBUG else 1  # 1 dia para teste

            if days_since_last >= required_days:
                # Escolher uma mensagem aleatória
                message = random.choice(MUNDO_ANIMAL_MESSAGES)

                # Escolher uma hora aleatória entre 15h e 23h
                send_hour = random.randint(
                    15, 22
                )  # 22 para garantir que a hora não ultrapasse 23h após random minutos
                send_minute = random.randint(0, 59)

                # Calcular o tempo atual e o tempo de envio
                send_time = now.replace(
                    hour=send_hour, minute=send_minute, second=0, microsecond=0
                )

                # Se o tempo de envio já passou hoje, agendar para amanhã
                if send_time < now:
                    send_time += datetime.timedelta(days=1)

                delay = (send_time - now).total_seconds()

                self.task_mundo_animal_logger.info(
                    f"Mensagem MUNDO ANIMAL agendada para {send_time.strftime('%Y-%m-%d %H:%M:%S')}."
                )

                # Esperar até o tempo de envio
                await asyncio.sleep(delay)

                # Enviar a mensagem
                channel = self.bot.get_channel(CANAL_DOIS_ID)

                if channel:
                    try:
                        await channel.send(message)
                        self.task_mundo_animal_logger.info(
                            f"Mensagem MUNDO ANIMAL enviada no canal {CANAL_DOIS_ID} às {send_time.strftime('%H:%M:%S')}."
                        )
                        print(
                            f"[{send_time.strftime('%Y-%m-%d %H:%M:%S')}] Mensagem MUNDO ANIMAL enviada no canal {CANAL_DOIS_ID}."
                        )

                        # Atualizar a última data de envio no banco de dados
                        if setting:
                            setting.value = today.strftime("%Y-%m-%d")
                        else:
                            new_setting = Settings(
                                key="last_mundo_animal_sent",
                                value=today.strftime("%Y-%m-%d"),
                            )
                            session.add(new_setting)
                        session.commit()
                    except Exception as e:
                        self.task_mundo_animal_logger.exception(
                            f"Erro ao enviar mensagem MUNDO ANIMAL: {e}"
                        )
                else:
                    self.task_mundo_animal_logger.error(
                        f"Canal com ID {CANAL_DOIS_ID} não encontrado."
                    )
                    print(f"Canal com ID {CANAL_DOIS_ID} não encontrado.")
            else:
                self.task_mundo_animal_logger.info(
                    f"Ainda faltam {required_days - days_since_last} dias para a próxima mensagem MUNDO ANIMAL."
                )
                print(
                    f"Ainda faltam {required_days - days_since_last} dias para a próxima mensagem MUNDO ANIMAL."
                )
        except Exception as e:
            self.task_mundo_animal_logger.exception(
                f"Erro na task mundo_animal_task: {e}"
            )

    @mundo_animal_task.before_loop
    async def before_mundo_animal_task(self):
        await self.bot.wait_until_ready()
        self.task_mundo_animal_logger.info("Tarefa MUNDO ANIMAL iniciada.")
        print("Tarefa MUNDO ANIMAL iniciada.")

    # Método auxiliar para obter o tempo atual com fuso horário
    def get_now(self):
        return datetime.datetime.now(TIMEZONE)  # cogs/tasks_cog.py


import os
from google.oauth2.service_account import Credentials
import random
import datetime
import gspread
from discord.ext import tasks, commands
from config import (
    CHANNEL_IDS,
    GOOD_AFTERNOON_CHANNEL_ID,
    TIMEZONE,
    QUINZENAL_MESSAGES,
    SEMANAL_MESSAGES,
    AVISOS_GERAIS_CANAL,
    MENSAGENS_ALERTA_PONTO,
    REALOCACAO_CANAL,
    MENSAGENS_ALERTA_REALOCACAO,
    MENSAGENS_ALERTA_ORACLE_CONFIGURACAO,
    GOOGLE_SHEETS_CREDENTIALS,
    GOOGLE_SHEETS_SPREADSHEET,
    GOOGLE_SHEETS_WORKSHEET,
    CANAL_DOIS_ID,
    CAHAMADA_MESSAGES,  # Atualizado para CAHAMADA
    DEBUG,
)
import asyncio
from database import session
from models import Settings
import logging


# Função auxiliar para retornar a data/hora no fuso definido.
def get_now():
    return datetime.datetime.now(TIMEZONE)


# Função para conectar ao Google Sheets (em stand by)
def conectar_google_sheets():
    """Conecta-se ao Google Sheets e retorna a worksheet especificada."""
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(
            GOOGLE_SHEETS_CREDENTIALS, scopes=scopes
        )
        client = gspread.authorize(creds)
        sheet = client.open(GOOGLE_SHEETS_SPREADSHEET)
        worksheet = sheet.worksheet(GOOGLE_SHEETS_WORKSHEET)
        return worksheet
    except Exception as e:
        # O log de erro será tratado pela task que chama esta função
        raise e


class TasksCog(commands.Cog):
    def __init__(self, bot: commands.Bot, geral_logger: logging.Logger):
        self.bot = bot
        self.geral_logger = geral_logger

        # Configuração dos loggers específicos para cada task
        self.task_semanal_logger = self.setup_logger(
            "discord_bot.task_semanal", "task_semanal.log"
        )
        self.task_good_afternoon_logger = self.setup_logger(
            "discord_bot.task_good_afternoon", "task_good_afternoon.log"
        )
        self.task_ajustar_ponto_logger = self.setup_logger(
            "discord_bot.task_ajustar_ponto", "ajustar_ponto.log"
        )
        self.task_quinzenal_logger = self.setup_logger(
            "discord_bot.task_quinzenal", "quinzenal_message.log"
        )
        self.task_enviar_realocacao_ticket_logger = self.setup_logger(
            "discord_bot.task_enviar_realocacao_ticket", "enviar_realocacao_ticket.log"
        )
        self.task_oracle_configuracao_logger = self.setup_logger(
            "discord_bot.task_oracle_configuracao", "oracle_configuracao.log"
        )
        self.task_enviar_aviso_excel_logger = self.setup_logger(
            "discord_bot.task_enviar_aviso_excel", "enviar_aviso_excel.log"
        )
        self.task_cahamada_logger = self.setup_logger(
            "discord_bot.task_cahamada", "cahamada.log"
        )  # Novo logger

        # Iniciar as tasks (elas só rodam quando o bot está pronto).
        self.semanal_message_task.start()
        self.send_good_afternoon_message.start()
        self.ajustar_ponto_task.start()
        self.quinzenal_message_task.start()
        self.enviar_realocacao_ticket.start()
        self.oracle_configuracao_task.start()
        self.enviar_aviso_excel.start()
        self.cahamada_task.start()  # Iniciar a nova task

    def setup_logger(self, logger_name: str, log_filename: str) -> logging.Logger:
        """
        Configura um logger específico para uma task.
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        log_file_path = os.path.join("logs", log_filename)
        handler = logging.FileHandler(
            filename=log_file_path, encoding="utf-8", mode="a"
        )
        formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    # =====================================================
    # Evento: quando o bot estiver pronto
    # =====================================================
    @commands.Cog.listener()
    async def on_ready(self):
        self.geral_logger.info(
            f"INICIALIZAÇÃO - Cog de Tasks carregado! Bot conectado como {self.bot.user}"
        )
        print(
            f"INICIALIZAÇÃO - Cog de Tasks carregado! Bot conectado como {self.bot.user}"
        )

    # =====================================================
    # Tarefa: Mensagem Semanal (uma vez por semana, qualquer dia entre 09:00 e 18:00)
    # =====================================================
    @tasks.loop(hours=1)  # Executa a task a cada hora
    async def semanal_message_task(self):
        try:
            now = get_now()
            current_week = now.isocalendar()[1]  # Número da semana atual

            # Recuperar a última semana enviada do banco de dados
            setting = session.query(Settings).filter_by(key="last_week_sent").first()
            last_week_sent = int(setting.value) if setting else None

            if current_week != last_week_sent:
                current_hour = now.hour

                # Verifica se está entre 09:00 e 18:00
                if 9 <= current_hour < 18:
                    # Seleciona uma mensagem aleatória da lista semanal
                    message = random.choice(SEMANAL_MESSAGES)

                    # Enviar a mensagem para o canal especificado
                    channel = self.bot.get_channel(AVISOS_GERAIS_CANAL)
                    if channel:
                        try:
                            await channel.send(message)
                            self.task_semanal_logger.info(
                                f"Mensagem semanal enviada no canal {AVISOS_GERAIS_CANAL} às {now.strftime('%H:%M:%S')}."
                            )
                            print(
                                f"[{now.strftime('%H:%M:%S')}] Enviada mensagem semanal no canal {AVISOS_GERAIS_CANAL}."
                            )

                            # Atualizar a semana enviada no banco de dados
                            if setting:
                                setting.value = str(current_week)
                            else:
                                new_setting = Settings(
                                    key="last_week_sent", value=str(current_week)
                                )
                                session.add(new_setting)
                            session.commit()
                        except Exception as e:
                            self.task_semanal_logger.exception(
                                f"Erro ao enviar mensagem semanal: {e}"
                            )
                            print(f"Erro ao enviar mensagem semanal: {e}")
                    else:
                        self.task_semanal_logger.error(
                            f"Canal com ID {AVISOS_GERAIS_CANAL} não encontrado."
                        )
                        print(f"Canal com ID {AVISOS_GERAIS_CANAL} não encontrado.")
            else:
                self.task_semanal_logger.info(
                    "Mensagem semanal já foi enviada esta semana."
                )
                print("Mensagem semanal já foi enviada esta semana.")
        except Exception as e:
            self.task_semanal_logger.exception(
                f"Erro na task semanal_message_task: {e}"
            )

    @semanal_message_task.before_loop
    async def before_semanal_message_task(self):
        await self.bot.wait_until_ready()
        self.task_semanal_logger.info("Tarefa semanal_message_task iniciada.")
        print("Tarefa semanal_message_task iniciada.")

    ## listar canais no discord
    def listar_canais_acessiveis(self):
        """
        Lista todos os canais que o bot pode acessar na guilda.
        """
        canais = []
        for guild in self.bot.guilds:
            for channel in guild.channels:
                canais.append((guild.name, channel.id, channel.name))
        return canais

    @commands.command(name="listar_canais")
    async def listar_canais(self, ctx):
        """
        Comando para listar todos os canais que o bot pode acessar.
        """
        canais = self.listar_canais_acessiveis()
        mensagem = "Canais que o bot pode acessar:\n"
        for guild_name, channel_id, channel_name in canais:
            mensagem += (
                f"Guilda: {guild_name} | ID: {channel_id} | Nome: {channel_name}\n"
            )
        await ctx.send(mensagem)

    # =====================================================
    # Tarefa de 15 em 15 minutos
    # =====================================================
    @tasks.loop(minutes=15)
    async def send_good_afternoon_message(self):
        try:
            now = get_now()
            message = f"@everyone teste chat funcional good afternoon de 15 em 15 minutos às ({now.strftime('%Y-%m-%d %H:%M:%S')})"

            channel = self.bot.get_channel(GOOD_AFTERNOON_CHANNEL_ID)
            if channel:
                try:
                    await channel.send(message)
                    self.task_good_afternoon_logger.info(
                        f"[{now.strftime('%H:%M:%S')}] Mensagem de teste enviada no canal {GOOD_AFTERNOON_CHANNEL_ID}."
                    )
                except Exception as e:
                    self.task_good_afternoon_logger.exception(
                        f"Erro ao enviar mensagem de teste: {e}"
                    )
            else:
                self.task_good_afternoon_logger.error(
                    f"Canal com ID {GOOD_AFTERNOON_CHANNEL_ID} não encontrado."
                )
        except Exception as e:
            self.task_good_afternoon_logger.exception(
                f"Erro na task send_good_afternoon_message: {e}"
            )

    # =====================================================
    # Tarefa para enviar lembrete de ajustar ponto
    # =====================================================
    @tasks.loop(minutes=1)
    async def ajustar_ponto_task(self):
        try:
            now = get_now()
            # Verifica se é dia 16, 17, 18, 19, 20 ou 21 e se o horário é 10:10 ou 18:14
            if now.day in [16, 17, 18, 19, 20, 21] and now.strftime("%H:%M") in [
                "10:10",
                "18:14",
            ]:
                # Seleciona uma mensagem aleatória da lista
                message = random.choice(MENSAGENS_ALERTA_PONTO)

                # Obtém o canal específico
                channel = self.bot.get_channel(AVISOS_GERAIS_CANAL)
                if channel:
                    try:
                        await channel.send(message)
                        self.task_ajustar_ponto_logger.info(
                            f"[{now.strftime('%Y-%m-%d %H:%M')}] Alerta de ponto enviado no canal {AVISOS_GERAIS_CANAL}."
                        )
                        print(
                            f"[{now.strftime('%Y-%m-%d %H:%M')}] Alerta de ponto enviado no canal {AVISOS_GERAIS_CANAL}."
                        )
                    except Exception as e:
                        self.task_ajustar_ponto_logger.exception(
                            f"Erro ao enviar alerta de ponto: {e}"
                        )
                else:
                    self.task_ajustar_ponto_logger.error(
                        f"Canal com ID {AVISOS_GERAIS_CANAL} não encontrado."
                    )
        except Exception as e:
            self.task_ajustar_ponto_logger.exception(
                f"Erro na task ajustar_ponto_task: {e}"
            )

    # =====================================================
    # Tarefa para enviar mensagem quinzenalmente
    # =====================================================
    @tasks.loop(hours=24)
    async def quinzenal_message_task(self):
        try:
            now = get_now()
            # Dia divisível por 15 (ex.: dia 15, 30, etc.)
            if now.day % 15 == 0:
                for channel_id in CHANNEL_IDS:
                    channel = self.bot.get_channel(channel_id)
                    if channel:
                        try:
                            await channel.send(QUINZENAL_MESSAGES[self.quinzenal_index])
                            self.task_quinzenal_logger.info(
                                f"[{now.strftime('%H:%M:%S')}] Enviada mensagem quinzenal no canal {channel_id}"
                            )
                            print(
                                f"[{now.strftime('%H:%M:%S')}] Enviada mensagem quinzenal no canal {channel_id}"
                            )
                        except Exception as e:
                            self.task_quinzenal_logger.exception(
                                f"Erro ao enviar mensagem quinzenal no canal {channel_id}: {e}"
                            )
                # Atualiza o índice (rotação circular)
                self.quinzenal_index = (self.quinzenal_index + 1) % len(
                    QUINZENAL_MESSAGES
                )
        except Exception as e:
            self.task_quinzenal_logger.exception(
                f"Erro na task quinzenal_message_task: {e}"
            )

    @quinzenal_message_task.before_loop
    async def before_quinzenal_message_task(self):
        await self.bot.wait_until_ready()
        self.task_quinzenal_logger.info("Tarefa quinzenal_message_task iniciada.")
        print("Tarefa quinzenal_message_task iniciada.")

    # =====================================================
    # Tarefa para enviar lembrete de realocação de ticket
    # =====================================================
    @tasks.loop(minutes=1)
    async def enviar_realocacao_ticket(self):
        try:
            now = get_now()
            # Verifica se é 09:00 da manhã
            if now.strftime("%H:%M") == "09:00":
                # Seleciona uma mensagem aleatória da lista específica
                message = random.choice(MENSAGENS_ALERTA_REALOCACAO)

                # Enviar a mensagem no canal específico
                channel = self.bot.get_channel(
                    REALOCACAO_CANAL
                )  # Substitua pelo canal correto
                if channel:
                    try:
                        await channel.send(message)
                        self.task_enviar_realocacao_ticket_logger.info(
                            f"Mensagem de realocação enviada no canal {REALOCACAO_CANAL} às {now.strftime('%H:%M:%S')}."
                        )
                        print(
                            f"Mensagem de realocação enviada no canal {REALOCACAO_CANAL} às {now.strftime('%H:%M:%S')}."
                        )
                    except Exception as e:
                        self.task_enviar_realocacao_ticket_logger.exception(
                            f"Erro ao enviar mensagem de realocação no canal {REALOCACAO_CANAL}: {e}"
                        )
                else:
                    self.task_enviar_realocacao_ticket_logger.error(
                        f"Canal com ID {REALOCACAO_CANAL} não encontrado."
                    )
        except Exception as e:
            self.task_enviar_realocacao_ticket_logger.exception(
                f"Erro na task enviar_realocacao_ticket: {e}"
            )

    # =====================================================
    # Task: Enviar Mensagem Oracle Configuração (Mensal)
    # =====================================================
    @tasks.loop(hours=1)  # Executa a task a cada hora
    async def oracle_configuracao_task(self):
        try:
            now = get_now()
            current_month = now.month  # Mês atual

            # Recuperar o último mês enviado do banco de dados
            setting = (
                session.query(Settings).filter_by(key="last_month_oracle_sent").first()
            )
            last_month_sent = int(setting.value) if setting else None

            if current_month != last_month_sent:
                current_hour = now.hour
                # Verifica se está entre 09:00 e 18:00
                if 9 <= current_hour < 18:
                    # Seleciona uma mensagem aleatória da lista de configurações Oracle
                    message = random.choice(MENSAGENS_ALERTA_ORACLE_CONFIGURACAO)

                    # Enviar a mensagem para o canal especificado
                    channel = self.bot.get_channel(
                        AVISOS_GERAIS_CANAL
                    )  # Substitua pelo canal correto
                    if channel:
                        try:
                            await channel.send(message)
                            self.task_oracle_configuracao_logger.info(
                                f"Mensagem Oracle enviada no canal {AVISOS_GERAIS_CANAL} às {now.strftime('%H:%M:%S')}."
                            )
                            print(
                                f"[{now.strftime('%H:%M:%S')}] Enviada mensagem Oracle no canal {AVISOS_GERAIS_CANAL}."
                            )

                            # Atualizar o mês enviado no banco de dados
                            if setting:
                                setting.value = str(current_month)
                            else:
                                new_setting = Settings(
                                    key="last_month_oracle_sent",
                                    value=str(current_month),
                                )
                                session.add(new_setting)
                            session.commit()
                        except Exception as e:
                            self.task_oracle_configuracao_logger.exception(
                                f"Erro ao enviar mensagem Oracle: {e}"
                            )
                            print(f"Erro ao enviar mensagem Oracle: {e}")
                    else:
                        self.task_oracle_configuracao_logger.error(
                            f"Canal com ID {AVISOS_GERAIS_CANAL} não encontrado."
                        )
                        print(f"Canal com ID {AVISOS_GERAIS_CANAL} não encontrado.")
            else:
                self.task_oracle_configuracao_logger.info(
                    "Mensagem Oracle já foi enviada este mês."
                )
                print("Mensagem Oracle já foi enviada este mês.")
        except Exception as e:
            self.task_oracle_configuracao_logger.exception(
                f"Erro na task oracle_configuracao_task: {e}"
            )

    @oracle_configuracao_task.before_loop
    async def before_oracle_configuracao_task(self):
        await self.bot.wait_until_ready()
        self.task_oracle_configuracao_logger.info(
            "Tarefa oracle_configuracao_task iniciada."
        )
        print("Tarefa oracle_configuracao_task iniciada.")

    # =====================================================
    # Task: Enviar Aviso a partir do Google Sheets
    # =====================================================
    @tasks.loop(minutes=15)  # Temporariamente rodando a cada minuto para testes
    async def enviar_aviso_excel(self):
        try:
            self.task_enviar_aviso_excel_logger.info(
                "Iniciando a execução da task 'enviar_aviso_excel'."
            )
            worksheet = conectar_google_sheets()
            if worksheet is None:
                self.task_enviar_aviso_excel_logger.error(
                    "Não foi possível conectar ao Google Sheets."
                )
                return

            # Obter todas as linhas da planilha como dicionários
            registros = worksheet.get_all_records()
            self.task_enviar_aviso_excel_logger.info(
                f"Número de registros encontrados na planilha: {len(registros)}."
            )

            for registro in registros:
                self.task_enviar_aviso_excel_logger.debug(
                    f"Processando registro: {registro}"
                )
                # Verificar se o aviso já foi enviado
                enviado = registro.get("Enviado", "").strip().upper()
                self.task_enviar_aviso_excel_logger.debug(
                    f"Aviso ID {registro.get('ID')}: Enviado = {enviado}"
                )

                if enviado != "TRUE":
                    canal_id = registro.get("Canal_ID")
                    mensagem = registro.get("Mensagem")
                    data_envio_str = registro.get("Data")
                    id_aviso = registro.get("ID")

                    # Validar campos essenciais
                    if not (canal_id and mensagem and data_envio_str and id_aviso):
                        self.task_enviar_aviso_excel_logger.warning(
                            f"Aviso com ID {id_aviso} possui campos incompletos. Pulando."
                        )
                        continue

                    # Converter string de data para objeto date
                    try:
                        data_envio = datetime.datetime.strptime(
                            data_envio_str, "%Y-%m-%d"
                        ).date()
                    except ValueError as ve:
                        self.task_enviar_aviso_excel_logger.error(
                            f"Formato de data inválido para aviso ID {id_aviso}: {data_envio_str}. Pulando."
                        )
                        continue

                    hoje = datetime.datetime.now().date()
                    self.task_enviar_aviso_excel_logger.debug(
                        f"Aviso ID {id_aviso}: Data de envio = {data_envio} | Data atual = {hoje}"
                    )

                    # Verificar se a data de envio é hoje
                    if data_envio == hoje:
                        try:
                            canal = self.bot.get_channel(int(canal_id))
                            if canal:
                                await canal.send(mensagem)
                                self.task_enviar_aviso_excel_logger.info(
                                    f"Mensagem enviada para o canal {canal_id}: {mensagem}"
                                )
                                print(
                                    f"Mensagem enviada para o canal {canal_id}: {mensagem}"
                                )

                                # Atualizar a flag 'Enviado' na planilha
                                try:
                                    cell = worksheet.find(str(id_aviso))
                                    if cell:
                                        # Assumindo que a coluna 'Enviado' é a 5ª coluna (E)
                                        worksheet.update_cell(cell.row, 5, "TRUE")
                                        self.task_enviar_aviso_excel_logger.info(
                                            f"Aviso ID {id_aviso} marcado como enviado."
                                        )
                                    else:
                                        self.task_enviar_aviso_excel_logger.error(
                                            f"Aviso ID {id_aviso} não encontrado na planilha."
                                        )
                                except Exception as update_exc:
                                    self.task_enviar_aviso_excel_logger.exception(
                                        f"Erro ao atualizar a planilha para aviso ID {id_aviso}: {update_exc}"
                                    )
                            else:
                                self.task_enviar_aviso_excel_logger.error(
                                    f"Canal com ID {canal_id} não encontrado."
                                )
                                print(f"Canal com ID {canal_id} não encontrado.")
                        except Exception as send_exc:
                            self.task_enviar_aviso_excel_logger.exception(
                                f"Erro ao enviar mensagem para o canal {canal_id}: {send_exc}"
                            )
        except Exception as e:
            self.task_enviar_aviso_excel_logger.exception(
                f"Erro na task enviar_aviso_excel: {e}"
            )
            print(f"Erro na task enviar_aviso_excel: {e}")

    @enviar_aviso_excel.before_loop
    async def before_enviar_aviso_excel(self):
        await self.bot.wait_until_ready()
        self.task_enviar_aviso_excel_logger.info("Tarefa enviar_aviso_excel iniciada.")
        print("Tarefa enviar_aviso_excel iniciada.")

    # =====================================================
    # Task: CAHAMADA (Enviar mensagem a cada 10 dias)
    # =====================================================
    @tasks.loop(hours=24)  # Executa a task diariamente
    async def cahamada_task(self):
        try:
            now = self.get_now()
            today = now.date()

            # Recuperar a última data de envio do banco de dados
            setting = (
                session.query(Settings).filter_by(key="last_cahamada_sent").first()
            )
            last_sent_date = (
                datetime.datetime.strptime(setting.value, "%Y-%m-%d").date()
                if setting
                else None
            )

            if setting:
                days_since_last = (today - last_sent_date).days
            else:
                days_since_last = 10  # Força o envio na primeira execução

            # Definir o intervalo de dias com base na flag DEBUG
            required_days = 10 if not DEBUG else 1  # 1 dia para teste

            if days_since_last >= required_days:
                # Escolher uma mensagem aleatória
                message = random.choice(CAHAMADA_MESSAGES)

                # Escolher uma hora aleatória entre 15h e 23h
                send_hour = random.randint(
                    15, 22
                )  # 22 para garantir que a hora não ultrapasse 23h após random minutos
                send_minute = random.randint(0, 59)

                # Calcular o tempo atual e o tempo de envio
                send_time = now.replace(
                    hour=send_hour, minute=send_minute, second=0, microsecond=0
                )

                # Se o tempo de envio já passou hoje, agendar para amanhã
                if send_time < now:
                    send_time += datetime.timedelta(days=1)

                delay = (send_time - now).total_seconds()

                self.task_cahamada_logger.info(
                    f"Mensagem CAHAMADA agendada para {send_time.strftime('%Y-%m-%d %H:%M:%S')}."
                )

                # Esperar até o tempo de envio
                await asyncio.sleep(delay)

                # Enviar a mensagem
                channel = self.bot.get_channel(CANAL_DOIS_ID)

                if channel:
                    try:
                        await channel.send(message)
                        self.task_cahamada_logger.info(
                            f"Mensagem CAHAMADA enviada no canal {CANAL_DOIS_ID} às {send_time.strftime('%H:%M:%S')}."
                        )
                        print(
                            f"[{send_time.strftime('%Y-%m-%d %H:%M:%S')}] Mensagem CAHAMADA enviada no canal {CANAL_DOIS_ID}."
                        )

                        # Atualizar a última data de envio no banco de dados
                        if setting:
                            setting.value = today.strftime("%Y-%m-%d")
                        else:
                            new_setting = Settings(
                                key="last_cahamada_sent",
                                value=today.strftime("%Y-%m-%d"),
                            )
                            session.add(new_setting)
                        session.commit()
                    except Exception as e:
                        self.task_cahamada_logger.exception(
                            f"Erro ao enviar mensagem CAHAMADA: {e}"
                        )
                else:
                    self.task_cahamada_logger.error(
                        f"Canal com ID {CANAL_DOIS_ID} não encontrado."
                    )
                    print(f"Canal com ID {CANAL_DOIS_ID} não encontrado.")
            else:
                self.task_cahamada_logger.info(
                    f"Ainda faltam {required_days - days_since_last} dias para a próxima mensagem CAHAMADA."
                )
                print(
                    f"Ainda faltam {required_days - days_since_last} dias para a próxima mensagem CAHAMADA."
                )
        except Exception as e:
            self.task_cahamada_logger.exception(f"Erro na task cahamada_task: {e}")

    @cahamada_task.before_loop
    async def before_cahamada_task(self):
        await self.bot.wait_until_ready()
        self.task_cahamada_logger.info("Tarefa CAHAMADA iniciada.")
        print("Tarefa CAHAMADA iniciada.")

    # Método auxiliar para obter o tempo atual com fuso horário
    def get_now(self):
        return datetime.datetime.now(TIMEZONE)

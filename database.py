# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Criação do engine para conectar ao SQLite (banco de dados local)
engine = create_engine('sqlite:///bot_database.db', echo=False)

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

# Criação de uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

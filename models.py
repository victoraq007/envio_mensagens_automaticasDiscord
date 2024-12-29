# models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    key = Column(String(50), unique=True, nullable=False)
    value = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Settings(key='{self.key}', value='{self.value}')>"

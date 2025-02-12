from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime  # Явный импорт datetime
import config

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    timezone = Column(String)
    weekly_report = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.now)  # Исправлено: datetime.now без скобок

class Habit(Base):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String)
    frequency = Column(String)
    days = Column(JSON)
    interval = Column(Integer)
    time = Column(String)
    motivation_type = Column(String)
    motivation_data = Column(String)
    created = Column(DateTime, default=datetime.now)  # Исправлено
    last_check = Column(DateTime)  # Разрешено NULL

class Stats(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer)
    date = Column(DateTime)
    status = Column(String)

# Инициализация движка и создание таблиц
engine = create_engine(config.DATABASE_URL)
Base.metadata.create_all(engine)  # Создает все таблицы после объявления классов
Session = sessionmaker(bind=engine)
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import config

Base = declarative_base()

class User(Base):  # Проверьте написание: User, а не Users или user
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    timezone = Column(String)
    weekly_report = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.now)

class Habit(Base):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String)
    frequency = Column(String)
    days = Column(JSON)  # Для еженедельных (список дней)
    interval = Column(Integer)  # Для интервальных
    time = Column(String)  # В формате HH:MM
    motivation_type = Column(String)  # text/voice/video
    motivation_data = Column(String)  # text или file_id
    created = Column(DateTime, default=datetime.now)
    last_check = Column(DateTime)

class Stats(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer)
    date = Column(DateTime)
    status = Column(String)  # done/missed

engine = create_engine(config.DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

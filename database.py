import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

Base = declarative_base()

# выбор конфига для подключения БД в зависимости от окружения
config = os.environ.get("CONFIG")
if config == "HEROKU":
    # подключение к Heroku Postgres
    url = os.environ.get("DATABASE_URL")
else:
    # подключение на тестовом сервере
    DB_NAME = os.environ.get("DB_NAME")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    url = URL(
        drivername="postgresql",
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host='localhost',
        port=5432,
        database=DB_NAME
    )

engine = create_engine(url,echo=True)
session = Session(engine)
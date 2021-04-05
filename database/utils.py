import os
def get_url():
    # выбор конфига для подключения БД в зависимости от окружения
    configuration = os.environ.get("CONFIG")
    if configuration == "HEROKU":
        # подключение к Heroku Postgres
        
        url = "postgresql" + os.environ.get("DATABASE_URL")[8:]
    else:
        # подключение на тестовом сервере
        from config import settings
        url = f'postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@localhost:5432/{settings.DB_NAME}'
    return url
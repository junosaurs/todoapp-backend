from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str

try:
    settings = Settings(_env_file=".env")
    test_settings = Settings(_env_file=".test_env")
finally:
    pass
import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestSettings(BaseSettings):
    host_db: str = Field(..., env='DB_HOST')
    port_db: int = Field(..., env='DB_PORT')
    user_db: str = Field(..., env='POSTGRES_USER')
    password_db: str = Field(..., env='POSTGRES_PASSWORD')
    name_db: str = Field(..., env='POSTGRES_DB')

    host_api: str = Field(..., env='API_HOST')
    port_api: int = Field(..., env='API_PORT')

    # Для локального запуска тестов
    class Config:
        env_file = os.path.join(BASE_DIR, './.env.test')


test_settings = TestSettings()

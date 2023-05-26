import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestSettings(BaseSettings):
    host: str = Field(..., env='DB_HOST')
    port: int = Field(..., env='DB_PORT')
    user: str = Field(..., env='DB_USER')
    password: str = Field(..., env='DB_PASSWORD')
    database: str = Field(..., env='DB_NAME')

    api_host: str = Field(..., env='API_HOST')
    api_port: int = Field(..., env='API_PORT')

    # Для локального запуска тестов
    class Config:
        env_file = os.path.join(BASE_DIR, '.env.test')


test_settings = TestSettings()

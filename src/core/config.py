import os

from pydantic import BaseSettings, Field, PostgresDsn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RedisConfig(BaseSettings):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')
    password: str = Field(..., env='REDIS_PASSWORD')


class PostgresConfig(BaseSettings):
    host: str = Field(..., env='DB_HOST')
    port: int = Field(..., env='DB_PORT')
    user: str = Field(..., env='DB_USER')
    password: str = Field(..., env='DB_PASSWORD')
    database: str = Field(..., env='DB_NAME')


pg_conf = PostgresConfig()


class AppConfig(BaseSettings):
    # base_dir: str = BASE_DIR
    # host: str = Field(..., env='APP_HOST')
    # port: int = Field(..., env='APP_PORT')
    # is_debug: bool = Field(..., env='IS_DEBUG')
    # pg: PostgresDsn = PostgresDsn.build(...)
    SQLALCHEMY_DATABASE_URI: PostgresDsn =\
        f'postgresql://{pg_conf.user}:{pg_conf.password}@{pg_conf.host}:{pg_conf.port}/{pg_conf.database}'
    JWT_SECRET_KEY: str = Field(..., env='JWT_SECRET_KEY')

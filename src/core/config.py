import datetime
from pydantic import BaseSettings, Field, PostgresDsn, validator


class JaegerConfig(BaseSettings):
    host: str = Field(..., env='JAEGER_HOST')
    port: int = Field(..., env='JAEGER_PORT')


class RedisConfig(BaseSettings):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')


class PostgresConfig(BaseSettings):
    host: str = Field(..., env='DB_HOST')
    port: int = Field(..., env='DB_PORT')
    user: str = Field(..., env='DB_USER')
    password: str = Field(..., env='DB_PASSWORD')
    database: str = Field(..., env='DB_NAME')
    host_local: str = Field(..., env='DB_HOST_LOCAL')


pg_conf = PostgresConfig()


class AppConfig(BaseSettings):
    SQLALCHEMY_DATABASE_URI: PostgresDsn =\
        f'postgresql://{pg_conf.user}:{pg_conf.password}@{pg_conf.host}:{pg_conf.port}/{pg_conf.database}'  # .build(..)
    JWT_SECRET_KEY: str = Field(..., env='JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES: datetime.timedelta = Field(..., env='ACCESS_TOKEN_TTL_IN_MINUTES')
    JWT_REFRESH_TOKEN_EXPIRES: datetime.timedelta = Field(..., env='REFRESH_TOKEN_TTL_IN_DAYS')

    @validator('JWT_ACCESS_TOKEN_EXPIRES', pre=True)
    def set_datetime_unit_minutes(cls, val):
        num_val = float(val)
        return datetime.timedelta(minutes=num_val)

    @validator('JWT_REFRESH_TOKEN_EXPIRES', pre=True)
    def set_datetime_unit_days(cls, val):
        return datetime.timedelta(days=float(val))


app_config = AppConfig()
jaeger_config = JaegerConfig()

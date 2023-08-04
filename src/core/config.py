import datetime

from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn, validator
from dotenv import load_dotenv

load_dotenv()


class JaegerConfig(BaseSettings):
    host: str = Field(..., env='JAEGER_HOST')
    port: int = Field(..., env='JAEGER_PORT')


class RedisConfig(BaseSettings):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')


class PostgresConfig(BaseSettings):
    host: str = Field(..., env='DB_HOST')
    port: int = Field(..., env='DB_PORT')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    database: str = Field(..., env='POSTGRES_DB')
    host_local: str = Field(..., env='DB_HOST_LOCAL')


pg_conf = PostgresConfig()
redis_conf = RedisConfig()


class AppConfig(BaseSettings):
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    SQLALCHEMY_DATABASE_URI: PostgresDsn = \
        f'postgresql://{pg_conf.user}:{pg_conf.password}@{pg_conf.host}:{pg_conf.port}/{pg_conf.database}'  # .build(..)
    JWT_SECRET_KEY: str = Field(..., env='JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES: datetime.timedelta = Field(..., env='ACCESS_TOKEN_TTL_IN_MINUTES')
    JWT_REFRESH_TOKEN_EXPIRES: datetime.timedelta = Field(..., env='REFRESH_TOKEN_TTL_IN_DAYS')

    RATELIMIT_STORAGE_URL: RedisDsn = f'redis://{redis_conf.host}:{redis_conf.port}/0'
    RATELIMIT_STRATEGY: str = 'fixed-window'
    RATELIMIT_HEADERS_ENABLED: bool = True
    RATELIMIT_DEFAULT: str = '20/minute'

    LOGSTASH_HOST: str = Field(..., env='LOGSTASH_HOST')
    LOGSTASH_PORT: int = Field(..., env='LOGSTASH_PORT')

    enable_tracer: bool = True

    @validator('JWT_ACCESS_TOKEN_EXPIRES', pre=True)
    def set_datetime_unit_minutes(cls, val):
        num_val = float(val)
        return datetime.timedelta(minutes=num_val)

    @validator('JWT_REFRESH_TOKEN_EXPIRES', pre=True)
    def set_datetime_unit_days(cls, val):
        return datetime.timedelta(days=float(val))


class OauthConfig(BaseSettings):
    google_client_id: str = Field(..., env='GOOGLE_CLIENT_ID')
    google_client_secret: str = Field(..., env='GOOGLE_CLIENT_SECRET')

    yandex_client_id: str = Field(..., env='YANDEX_CLIENT_ID')
    yandex_client_secret: str = Field(..., env='YANDEX_CLIENT_SECRET')


class SentryConfig(BaseSettings):
    dns: str = Field(..., env='SENTRY_DSN')


oauth_config = OauthConfig()
app_config = AppConfig()
jaeger_config = JaegerConfig()
sentry_config = SentryConfig()

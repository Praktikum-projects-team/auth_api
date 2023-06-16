import datetime
from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn, validator


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

    @validator('JWT_ACCESS_TOKEN_EXPIRES', pre=True)
    def set_datetime_unit_minutes(cls, val):
        num_val = float(val)
        return datetime.timedelta(minutes=num_val)

    @validator('JWT_REFRESH_TOKEN_EXPIRES', pre=True)
    def set_datetime_unit_days(cls, val):
        return datetime.timedelta(days=float(val))


app_config = AppConfig()
jaeger_config = JaegerConfig()

class OauthConfig(BaseSettings):
    OAUTHLIB_INSECURE_TRANSPORT: int = Field(..., env='OAUTHLIB_INSECURE_TRANSPORT')
    OAUTHLIB_RELAX_TOKEN_SCOPE: int = Field(..., env='OAUTHLIB_RELAX_TOKEN_SCOPE')
    API_SERVICE_NAME: str = Field(..., env='API_SERVICE_NAME')
    API_VERSION: str = Field(..., env='API_VERSION')
    SCOPES: str = Field(..., env='SCOPES')


oauth_config = OauthConfig()

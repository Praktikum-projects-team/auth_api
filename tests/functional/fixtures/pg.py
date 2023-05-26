import pytest
import psycopg2

from core.config import PostgresConfig

pg_conf = PostgresConfig()


@pytest.fixture(scope="session")
def postgres_conn():
    conn = psycopg2.connect(
        database=pg_conf.database,
        user=pg_conf.user,
        password=pg_conf.password,
        host=pg_conf.host_local,
        port=pg_conf.port
    )
    yield conn
    conn.close()

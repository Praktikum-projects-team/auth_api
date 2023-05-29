import pytest
import psycopg2

from tests.functional.settings import TestSettings

test_conf = TestSettings()


@pytest.fixture(scope="session")
def postgres_conn():
    conn = psycopg2.connect(
        database=test_conf.name_db,
        user=test_conf.user_db,
        password=test_conf.password_db,
        host=test_conf.host_db,
        port=test_conf.port_db
    )
    yield conn
    conn.close()

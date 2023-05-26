import backoff
import psycopg2

from tests.functional.settings import test_settings


@backoff.on_exception(
    backoff.expo,
    psycopg2.OperationalError,
    max_tries=10,
)
def wait_postgres(postgres_client):
    postgres_client.cursor().execute('SELECT 1')


if __name__ == '__main__':
    postgres_client = psycopg2.connect(
        host=test_settings.postgres_host,
        port=test_settings.postgres_port,
        user=test_settings.postgres_user,
        password=test_settings.postgres_password,
        database=test_settings.postgres_database,
    )
    wait_postgres(postgres_client)

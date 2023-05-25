import argparse
import uuid
from datetime import datetime
import logging

import psycopg2

from core.config import PostgresConfig

parser = argparse.ArgumentParser(description='Create superuser')
parser.add_argument('login', type=str, help='Superuser login')
parser.add_argument('password', type=str, help='Superuser password')

args = parser.parse_args()

pg_conf = PostgresConfig()
conn = psycopg2.connect(
    database=pg_conf.database,
    user=pg_conf.user,
    password=pg_conf.password,
    host=pg_conf.host_local,
    port=pg_conf.port
)


def createsuperuser(login, password):
    user_id = str(uuid.uuid4())

    with conn.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE login = %s)", (login,))
        user_exist = cursor.fetchone()[0]
    if user_exist:
        logging.warning("Superuser already exist")
        return "Superuser already exist"

    with conn.cursor() as cursor:
        created_at = datetime.utcnow()
        cursor.execute(
            "INSERT INTO users (id, login, password, is_superuser, created_at)"
            "VALUES (%s, %s, %s, %s, %s)",
            (user_id, login, password, True, created_at)
        )
        conn.commit()

    conn.close()

    logging.warning("Superuser successfully created")
    return "Superuser successfully created"


if __name__ == '__main__':
    createsuperuser(args.login, args.password)

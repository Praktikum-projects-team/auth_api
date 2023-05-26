import os
from dotenv import load_dotenv

ABS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ABS_DIR, '.env'))

import argparse
import logging
import uuid
from datetime import datetime

import psycopg2

from core.config import PostgresConfig

logging.basicConfig(level=logging.INFO)

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
        return

    with conn.cursor() as cursor:
        created_at = datetime.utcnow()
        cursor.execute(
            "INSERT INTO users (id, login, password, is_superuser, created_at)"
            "VALUES (%s, %s, %s, %s, %s)",
            (user_id, login, password, True, created_at)  # TODO hash password after merging auth
        )
        conn.commit()

    conn.close()

    logging.info("Superuser successfully created")


if __name__ == '__main__':
    createsuperuser(args.login, args.password)

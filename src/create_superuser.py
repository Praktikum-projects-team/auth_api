import os
from dotenv import load_dotenv

from constants import RoleName
from services.auth.passwords import hash_password

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
    hashed_password = hash_password(password)

    with conn.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE login = %s)", (login,))
        user = cursor.fetchone()[0]
    if user:
        logging.warning("Superuser already exist")
        return

    # Создаем суперпользователя, если он не был создан
    with conn.cursor() as cursor:
        created_at = datetime.utcnow()
        cursor.execute(
            "INSERT INTO users (id, login, password, is_superuser, created_at)"
            "VALUES (%s, %s, %s, %s, %s)",
            (user_id, login, hashed_password, True, created_at)
        )
        conn.commit()

    # Создаем роль администратора, если она не была создана
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM roles WHERE name = %s", (RoleName.ADMIN,)
        )
        role = cursor.fetchone()
    if not role:
        role_id = str(uuid.uuid4())
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO roles (id, name)"
                "VALUES (%s, %s)",
                (role_id, RoleName.ADMIN,)
            )
            conn.commit()
    else:
        # Получаем id созданной роли администратора
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM roles WHERE name = %s", (RoleName.ADMIN,)
            )
            role_id = cursor.fetchone()

    # Привязываем роль администратора к суперпользователю
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO user_roles (user_id, role_id, given_at)"
            "VALUES (%s, %s, %s)",
            (user_id, role_id, datetime.utcnow())
        )
        conn.commit()

    conn.close()

    logging.info("Superuser successfully created")


if __name__ == '__main__':
    createsuperuser(args.login, args.password)

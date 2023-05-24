import argparse
import uuid
from datetime import datetime

import psycopg2

from constants import RoleName
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
    role_id = str(uuid.uuid4())

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE login = %s", (login,))
        user_exist = cursor.fetchone()
    if user_exist:
        return "Superuser already exist"

    with conn.cursor() as cursor:
        created_at = datetime.utcnow()
        cursor.execute(
            "INSERT INTO users (id, login, password, is_superuser, created_at)"
            "VALUES (%s, %s, %s, %s, %s)",
            (user_id, login, password, True, created_at)
        )
        conn.commit()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM roles WHERE name = %s", (RoleName.ADMIN,))
        role_exist = cursor.fetchone()

    if not role_exist:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO roles (id, name) VALUES (%s, %s)", (role_id, RoleName.ADMIN,))
            conn.commit()
    else:
        role_id = role_exist[0]

    given_at = datetime.utcnow()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO user_roles (role_id, user_id, given_at)"
            "VALUES (%s, %s, %s)",
            (role_id, user_id, given_at)
        )
        conn.commit()

    conn.close()

    return "Superuser successfully created"


if __name__ == '__main__':
    createsuperuser(args.login, args.password)

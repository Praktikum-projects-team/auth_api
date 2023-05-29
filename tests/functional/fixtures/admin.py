import logging
import uuid
from datetime import datetime

import pytest
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from tests.functional.utils.constants import AdminData, RoleName


@pytest.fixture(scope="session", autouse=True)
def create_admin(pg_conn):
    user_id = str(uuid.uuid4())
    hashed_password = pbkdf2_sha256.hash(AdminData.PASSWORD)

    with pg_conn.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE login = %s)", (AdminData.LOGIN,))
        user = cursor.fetchone()[0]
    if user:
        logging.warning("Superuser already exist")
        return

    # Создаем админа для тесовой сессии, если он не был создан
    with pg_conn.cursor() as cursor:
        created_at = datetime.utcnow()
        cursor.execute(
            "INSERT INTO users (id, login, password, is_superuser, created_at)"
            "VALUES (%s, %s, %s, %s, %s)",
            (user_id, AdminData.LOGIN, hashed_password, True, created_at)
        )
        pg_conn.commit()

    # Создаем роль администратора, если она не была создана
    with pg_conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM roles WHERE name = %s", (RoleName.ADMIN,)
        )
        role = cursor.fetchone()
    if not role:
        role_id = str(uuid.uuid4())
        with pg_conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO roles (id, name)"
                "VALUES (%s, %s)",
                (role_id, RoleName.ADMIN,)
            )
            pg_conn.commit()
    else:
        # Получаем id созданной роли администратора
        with pg_conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM roles WHERE name = %s", (RoleName.ADMIN,)
            )
            role_id = cursor.fetchone()

    # Привязываем роль администратора к суперпользователю
    with pg_conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO user_roles (user_id, role_id, given_at)"
            "VALUES (%s, %s, %s)",
            (user_id, role_id, datetime.utcnow())
        )
        pg_conn.commit()

    pg_conn.close()

    logging.info("Superuser successfully created")

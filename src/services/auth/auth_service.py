from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token

from core.config import app_config
from db.queries.user import get_user_by_login, add_login_history_record
from db.queries.user import create_new_user
from db.pg_db import db
from services.auth.passwords import hash_password, verify_password
from services.auth.jwt_init import jwt
from db.redis_storage import jwt_redis_blocklist


class UserAlreadyExists(Exception):
    ...


class UserIncorrectLoginData(Exception):
    ...


class UserIncorrectPassword(Exception):
    ...


# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


def add_token_to_block_list(jti, token_type):
    ttl = app_config.JWT_ACCESS_TOKEN_EXPIRES if token_type == 'access' else app_config.JWT_REFRESH_TOKEN_EXPIRES
    jwt_redis_blocklist.set(jti, "", ex=ttl)


def sign_up_user(user):
    user['password'] = hash_password(user['password'])
    try:
        create_new_user(user)
    except IntegrityError:
        raise UserAlreadyExists(f'user with login {user["login"]} already exists')


def generate_token_pair(identity):
    tokens = {
        'access_token': create_access_token(identity=identity),
        'refresh_token': create_refresh_token(identity=identity)
    }
    return tokens


def login_user(login: str, password: str, user_agent: str):
    user = get_user_by_login(login)
    if not user or not verify_password(password=password, hashed_password=user.password):
        raise UserIncorrectLoginData('login or password is incorrect')

    tokens = generate_token_pair(identity=user.login)
    add_login_history_record(user_id=user.id, user_agent=user_agent)
    return tokens


def change_user_pw(login: str, password: str, new_password: str):
    user = get_user_by_login(login)
    if verify_password(password=password, hashed_password=user.password):
        user.password = hash_password(new_password)
        db.session.commit()
    else:
        raise UserIncorrectPassword("Incorrect old password")

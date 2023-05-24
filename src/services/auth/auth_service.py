from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token


from db.queries.user import does_user_exist, get_user_by_login
from db.queries.user import create_new_user
from services.auth.passwords import hash_password, verify_password


class UserAlreadyExists(Exception):
    ...


class UserIncorrectLoginData(Exception):
    ...


def sign_up_user(user):
    user['password'] = hash_password(user['password'])
    try:
        create_new_user(user)
    except IntegrityError:
        raise UserAlreadyExists(f'user with login {user["login"]} already exists')


def login_user(login: str, password: str):
    user = get_user_by_login(login)
    if not user or not verify_password(password=password, hashed_password=user.password):
        raise UserIncorrectLoginData('login or password is incorrect')

    access_token = create_access_token(identity=user.login)
    return access_token
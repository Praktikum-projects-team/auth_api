import secrets


from flask import request

from db.pg_db import db
from db.models import OauthAccount, User
from db.queries.user import add_login_history_record
from services.auth.auth_service import generate_token_pair, sign_up_user


def get_oauth_user(user, provider):
    if provider == 'google':
        login = user['email']
        name = user.get('given_name')
    if provider == 'yandex':
        login = user['default_email']
        name = user.get('first_name')
    return {
        'login': login,
        'name': name,
    }


def create_oauth_account(oauth_user: dict, provider: str) -> User:
    user = User.query.filter_by(login=oauth_user['login']).first()
    if not user:
        user_info = oauth_user
        user_info['password'] = secrets.token_urlsafe(10)
        user = sign_up_user(user_info)

    oauth_account = OauthAccount(oauth_user_login=user.login, user_id=user.id, provider=provider)
    db.session.add(oauth_account)
    db.session.commit()
    return user


def login_by_oauth(oauth_user: dict[str, str], provider: str):
    oauth_account = OauthAccount.query.filter_by(oauth_user_login=oauth_user['login']).first()

    if not oauth_account:
        user = create_oauth_account(oauth_user=oauth_user, provider=provider)
    else:
        user = User.query.filter_by(id=oauth_account.user_id).first()
    add_login_history_record(user_id=user.id, user_agent=str(request.user_agent))

    return generate_token_pair(user.login)

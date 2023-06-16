from db.queries.user import get_user_by_login
from services.auth.auth_service import sign_up_user, generate_token_pair, add_login_history_record


def oauth_user_login(user, user_agent):
    tokens = generate_token_pair(identity=user.login)
    add_login_history_record(user_id=user.id, user_agent=user_agent)

    return tokens


def oauth_user(user_data, user_agent):
    user = get_user_by_login(user_data['login'])
    if not user:
        sign_up_user(user_data)

    return oauth_user_login(get_user_by_login(user_data['login']), user_agent)

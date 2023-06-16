from flask import Blueprint, url_for

from api.v1.models.auth import login_out
from core.oauth_init import oauth
from services.auth.oauth import login_by_oauth, get_oauth_user


oauth_bp = Blueprint("oauth_bp", __name__)


@oauth_bp.route('/<provider>/authorize')
def login(provider: str):
    redirect_uri = url_for('oauth_bp.authorize', _external=True, provider=provider)
    return oauth.google.authorize_redirect(redirect_uri)


@oauth_bp.route('/<provider>/oauth2callback')
def authorize(provider: str):
    token = oauth.google.authorize_access_token()
    # resp = oauth.google.get('userinfo', token=token)
    # user_info = resp.json()
    userinfo = oauth.google.userinfo()

    oauth_user = get_oauth_user(userinfo, provider)
    tokens = login_by_oauth(oauth_user, provider)
    return login_out.dump(tokens)

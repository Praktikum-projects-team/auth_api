from flask import Blueprint, url_for

from api.v1.models.auth import login_out
from core.oauth_init import oauth
from services.auth.oauth import login_by_oauth, get_oauth_user


oauth_bp = Blueprint("oauth_bp", __name__)


@oauth_bp.route('/<provider>/authorize')
def login(provider: str):
    redirect_uri = url_for('oauth_bp.authorize', _external=True, provider=provider)
    provider_client = oauth.create_client(provider)
    return provider_client.authorize_redirect(redirect_uri)


@oauth_bp.route('/<provider>/oauth2callback')
def authorize(provider: str):
    provider_client = oauth.create_client(provider)
    token = provider_client.authorize_access_token()
    # resp = oauth.google.get('userinfo', token=token)
    # user_info = resp.json()
    userinfo = provider_client.userinfo()

    oauth_user = get_oauth_user(userinfo, provider)
    tokens = login_by_oauth(oauth_user, provider)
    return login_out.dump(tokens)

import os
from http import HTTPStatus

from flask import Blueprint, url_for, jsonify, session, redirect
from marshmallow import ValidationError

from api.v1.models.auth import login_out
from core.oauth_init import oauth
from services.auth.oauth import login_by_oauth, get_oauth_user
from services.oauth.oauth_service import get_authorization_url, \
    set_google_oauth_credentials, authorize_user_with_google

CLIENT_SECRETS_FILE = os.path.abspath(os.path.dirname(__file__)) + '/client_secret.json'

oauth_bp = Blueprint("oauth_bp", __name__)



@oauth_bp.route('/<provider>/authorize')
def login(provider: str):
    redirect_uri = url_for('oauth_bp.authorize', _external=True, provider=provider)
    return oauth.google.authorize_redirect(redirect_uri)


@oauth_bp.route('/<provider>/oauth2callback')
def authorize(provider):
    token = oauth.google.authorize_access_token()
    # resp = oauth.google.get('userinfo', token=token)
    # user_info = resp.json()
    userinfo = oauth.google.userinfo()

    oauth_user = get_oauth_user(userinfo, provider)
    tokens = login_by_oauth(oauth_user, provider)
    return login_out.dump(tokens)

import os
from http import HTTPStatus
import logging

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from flask import Blueprint, url_for, jsonify, session, redirect, request
from marshmallow import ValidationError
import secrets

from api.v1.models.auth import login_out, login_in_oauth
from services.oauth.oauth_service import oauth_user, get_authorization_url, credentials_to_dict, \
    set_google_oauth_credentials, authorize_user_with_google
from core.config import oauth_config

CLIENT_SECRETS_FILE = os.path.abspath(os.path.dirname(__file__)) + '/client_secret.json'

oauth_bp = Blueprint("oauth_bp", __name__)


@oauth_bp.route('/google')
def oauth_google():
    try:
        tokens = authorize_user_with_google()
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.UNPROCESSABLE_ENTITY
    return login_out.dump(tokens)


@oauth_bp.route('/google/authorize')
def authorize():
    authorization_url = get_authorization_url(CLIENT_SECRETS_FILE)

    return redirect(authorization_url)


@oauth_bp.route('/google/oauth2callback')
def oauth2callback():
    set_google_oauth_credentials(CLIENT_SECRETS_FILE)

    return redirect('/api/v1/oauth/google')

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
from services.oauth.oauth_service import oauth_user
from core.config import oauth_config

CLIENT_SECRETS_FILE = os.path.abspath(os.path.dirname(__file__)) + '/client_secret.json'

oauth_bp = Blueprint("oauth_bp", __name__)


def authorize_user(user_email: str, provider: str):
    user_info = {"login": user_email, "password": secrets.token_urlsafe(10)}
    user_agent = request.headers.get('User-Agent', default='unknown device')

    try:
        user = login_in_oauth.load(user_info)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.UNPROCESSABLE_ENTITY

    tokens = oauth_user(user, user_agent)
    logging.info('User with email %s successfully logged in with %ss service', user['login'], provider)
    del session['credentials']

    return login_out.dump(tokens)


@oauth_bp.route('/google')
def oauth_google():
    if 'credentials' not in session:
        return redirect(url_for('oauth_bp.authorize'))
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])
    person_data = googleapiclient.discovery.build(
        oauth_config.API_SERVICE_NAME, oauth_config.API_VERSION, credentials=credentials, static_discovery=False)
    files = person_data.userinfo().get().execute()
    session['credentials'] = credentials_to_dict(credentials)

    return authorize_user(files['email'], 'google')


@oauth_bp.route('/google/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=oauth_config.SCOPES)
    flow.redirect_uri = url_for('oauth_bp.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)


@oauth_bp.route('/google/oauth2callback')
def oauth2callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=oauth_config.SCOPES, state=state)
    flow.redirect_uri = url_for('oauth_bp.oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect('/api/v1/oauth/google')


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

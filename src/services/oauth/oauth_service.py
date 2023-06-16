import logging
import secrets

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from db.queries.user import get_user_by_login
from flask import url_for, session, request
from services.auth.auth_service import sign_up_user, generate_token_pair, add_login_history_record
from core.config import oauth_config
from api.v1.models.auth import login_out, login_in_oauth


def oauth_user_login(user, user_agent):
    tokens = generate_token_pair(identity=user.login)
    add_login_history_record(user_id=user.id, user_agent=user_agent)

    return tokens


def oauth_user(user_data, user_agent):
    user = get_user_by_login(user_data['login'])
    if not user:
        sign_up_user(user_data)

    return oauth_user_login(get_user_by_login(user_data['login']), user_agent)


def get_authorization_url(client_secret):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secret, scopes=oauth_config.SCOPES)
    flow.redirect_uri = url_for('oauth_bp.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state

    return authorization_url


def set_google_oauth_credentials(client_secret):
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secret, scopes=oauth_config.SCOPES, state=state)
    flow.redirect_uri = url_for('oauth_bp.oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)


def authorize_user_with_google():
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])
    person_data = googleapiclient.discovery.build(
        oauth_config.API_SERVICE_NAME, oauth_config.API_VERSION, credentials=credentials, static_discovery=False)
    files = person_data.userinfo().get().execute()
    session['credentials'] = credentials_to_dict(credentials)

    return authorize_user(files['email'], 'google')


def authorize_user(user_email: str, provider: str):
    user_info = {"login": user_email, "password": secrets.token_urlsafe(10)}
    user_agent = request.headers.get('User-Agent', default='unknown device')
    user = login_in_oauth.load(user_info)

    tokens = oauth_user(user, user_agent)
    logging.info('User with email %s successfully logged in with %ss service', user['login'], provider)
    del session['credentials']

    return tokens


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

from __future__ import annotations
import os

from authlib.integrations.flask_client import OAuth as OAuthClient
from flask import Blueprint, url_for, session, redirect

OAuth = OAuthClient()

oauth_bp = Blueprint("google", __name__)


def create_oauth(app):
    OAuth.init_app(app=app)
    OAuth.register(
        name='google',
        client_id=os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'email'},
    )


@oauth_bp.route('/hello-world')
def hello_world():
    email = dict(session)['profile']['email']
    return f'Users email: {email}!'


@oauth_bp.route('/', methods=['GET'])
def login():
    google = OAuth.create_client('google')
    redirect_uri = url_for('google.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@oauth_bp.route('/authorize')
def authorize():
    google = OAuth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    user_info = resp.json()
    user = OAuth.google.userinfo()
    session['profile'] = user_info
    session.permanent = True
    return redirect('/api/v1/login/google/hello-world')




from __future__ import annotations
import os
from authlib.integrations.flask_client import OAuth

from http import HTTPStatus
from typing import Any

from pydantic import BaseModel

from flask import Blueprint, url_for, session, redirect, Response

from core.config import oauth_config

oauth = OAuth()


def init_oauth(app):
    oauth.init_app(app=app)
    oauth.register(
        name='google',
        client_id=oauth_config.google_client_id,
        client_secret=oauth_config.google_client_secret,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        # access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        # authorize_params=None,
        # api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'email'},
    )
    oauth.register(
        name='yandex',
        client_id=oauth_config.yandex_client_id,
        client_secret=oauth_config.yandex_client_secret,
        access_token_url='https://oauth.yandex.ru/token',
        authorize_url='https://oauth.yandex.ru/authorize'
    )

import logging

import logstash
import sentry_sdk
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import upgrade
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from sentry_sdk.integrations.flask import FlaskIntegration

from api.v1.admin_roles import admin_roles_bp
from api.v1.admin_users import admin_users_bp
from api.v1.auth import auth_bp
from api.v1.models.marshmallow_init import init_marshmallow
from api.v1.oauth import oauth_bp
from api.v1.users import users_bp
from core.config import app_config
from core.oauth_init import init_oauth
from core.tracing import configure_tracer
from db.alembic_migrate_init import init_migration_tool
from db.pg_db import db, init_db
from services.auth.jwt_init import init_jwt


def register_blueprints(app):
    API_V1_PATH = '/api/v1'
    app.register_blueprint(oauth_bp, url_prefix=API_V1_PATH + '/oauth')
    app.register_blueprint(auth_bp, url_prefix=API_V1_PATH + '/auth')
    app.register_blueprint(admin_roles_bp, url_prefix=API_V1_PATH + '/admin/roles')
    app.register_blueprint(users_bp, url_prefix=API_V1_PATH + '/user')
    app.register_blueprint(admin_users_bp, url_prefix=API_V1_PATH + '/admin/users')


def init_extensions(app):
    init_jwt(app=app)
    init_db(app=app)
    init_migration_tool(app=app, db=db)
    init_marshmallow(app=app)
    init_oauth(app)
    limiter = Limiter(key_func=get_remote_address)
    limiter.init_app(app)
    FlaskInstrumentor().instrument_app(app)
    sentry_sdk.init(
        dsn=app.config['SENTRY_DSN'],
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.4
    )


def config_log(app):
    app.logger = logging.getLogger(__name__)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(
        logstash.LogstashHandler(
            host=app.config['LOGSTASH_HOST'],
            port=app.config['LOGSTASH_PORT'],
            version=1,
        )
    )


if app_config.enable_tracer:
    configure_tracer()


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config)
    init_extensions(app)
    register_blueprints(app)
    with app.app_context():
        upgrade()
    config_log(app)
    return app


app = create_app()
logger = app.logger


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    app.logger = logging.LoggerAdapter(
        logger=logger,
        extra={'tags': ['auth_api'], 'X-Request-Id': request_id},
    )
    if not request_id:
        raise RuntimeError('request id is required')

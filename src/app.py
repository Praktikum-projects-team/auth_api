from flask import Flask, request
from flask_migrate import upgrade
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from api.v1.admin_roles import admin_roles_bp
from api.v1.admin_users import admin_users_bp
from api.v1.auth import auth_bp
from api.v1.users import users_bp
from api.v1.models.marshmallow_init import init_marshmallow
from core.config import app_config
from core.tracing import configure_tracer
from db.alembic_migrate_init import init_migration_tool
from db.pg_db import db, init_db
from services.auth.jwt_init import init_jwt


def register_blueprints(app):
    API_V1_PATH = '/api/v1'
    app.register_blueprint(auth_bp, url_prefix=API_V1_PATH + '/auth')
    app.register_blueprint(admin_roles_bp, url_prefix=API_V1_PATH + '/admin/roles')
    app.register_blueprint(users_bp, url_prefix=API_V1_PATH + '/user')
    app.register_blueprint(admin_users_bp, url_prefix=API_V1_PATH + '/admin/users')


def init_extensions(app):
    init_jwt(app=app)
    init_db(app=app)
    init_migration_tool(app=app, db=db)
    init_marshmallow(app=app)
    FlaskInstrumentor().instrument_app(app)


configure_tracer()


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config)
    init_extensions(app)
    register_blueprints(app)
    with app.app_context():
        upgrade()
    return app


app = create_app()


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')

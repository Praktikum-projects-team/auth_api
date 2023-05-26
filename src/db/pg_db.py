from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.config import PostgresConfig
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
pg_conf = PostgresConfig()
pg_dsn = f'postgresql://{pg_conf.user}:{pg_conf.password}@{pg_conf.host}:{pg_conf.port}/{pg_conf.database}'


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = pg_dsn
    db.init_app(app)

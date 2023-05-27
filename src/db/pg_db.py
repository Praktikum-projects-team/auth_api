from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()


def init_db(app: Flask):
    db.init_app(app)

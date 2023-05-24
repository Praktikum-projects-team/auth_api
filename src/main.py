# from flask import Flask
# from flask_marshmallow import Marshmallow
# from marshmallow import fields, Schema, validate
#
# from api.v1.role import roles
# from core import config
# from db.pg_db import db, init_db

# app_config = config.AppConfig()
# postgres_config = config.PostgresConfig()
# redis_config = config.RedisConfig()


# app = Flask(__name__)
# ma = Marshmallow(app)
# app.register_blueprint(roles, url_prefix="/api/v1/admin/roles")
# init_db(app=app)
#
# with app.app_context():
#     db.create_all()
#
#
# @app.route('/api/hello-world')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()

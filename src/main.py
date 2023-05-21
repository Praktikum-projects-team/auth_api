import requests
from flask import Flask

from core import config

app_config = config.AppConfig()
postgres_config = config.PostgresConfig()
redis_config = config.RedisConfig()


app = Flask(__name__)


@app.route('/api/hello-world')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()

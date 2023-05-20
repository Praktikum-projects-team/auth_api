import logging

import requests
import uvicorn
from flask import Flask

from core import config
from core.logger import LOGGING

app_config = config.AppConfig()
postgres_config = config.PostgresConfig()
redis_config = config.RedisConfig()


app = Flask(__name__)


@app.route('/hello-world')
def hello_world():
    requests.get('http://slow_application_host/slow-operation§')
    return 'Hello, World!'


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_config.host,
        port=app_config.port,
        log_config=LOGGING,
        log_level=logging.DEBUG if app_config.is_debug else logging.INFO,
    )

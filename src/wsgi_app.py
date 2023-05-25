from gevent import monkey
from app import create_app

monkey.patch_all()

app = create_app()


# Todo: удалить после написания всех апи, временно оставлено в качестве пинга
@app.route('/api/hello-world')
def hello_world():
    return 'Hello World!'

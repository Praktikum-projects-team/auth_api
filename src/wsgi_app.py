from gevent import monkey

monkey.patch_all()

from app import create_app

app = create_app()


# Todo: удалить после написания всех апи, временно оставлено в качестве пинга
@app.route('/api/hello-world')
def hello_world():
    return 'Hello World!'

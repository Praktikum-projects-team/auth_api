from gevent import monkey
from gevent.pywsgi import WSGIServer

from wsgi_app import app

monkey.patch_all()

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()

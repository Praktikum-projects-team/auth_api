from gevent import monkey
monkey.patch_all()

# from main import app
from app import create_app

app = create_app()

#src/app.py

from flask import Flask

from .config import app_config
from .models import db, bcrypt

def create_app(env_name):

    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    #wrapping bcrpyt with flask app object
    bcrypt.init_app(app)
    #wrapping SQLalchemy object with flask app object
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def index():
        return 'End point working!!'

    return app

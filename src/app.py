#src/app.py

from flask import Flask

from .config import app_config
from .models import db, bcrypt
from .views.userview import user_api as user_bp
from .views.blogpostview import posts_api as blogpost_bp
def create_app(env_name):

    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    #wrapping bcrpyt with flask app object
    bcrypt.init_app(app)
    #wrapping SQLalchemy object with flask app object
    db.init_app(app)
    #Registering new user_api
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(blogpost_bp, url_prefix='/api/posts')

    @app.route('/', methods=['GET'])
    def index():
        return 'End point working!!', 200

    return app

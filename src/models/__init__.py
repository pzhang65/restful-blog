#src/models/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize our db
db = SQLAlchemy()

# intialize bcrpyt for use in user-model.py
bcrypt = Bcrypt()

from .blogpostmodel import *
from .usermodel import *

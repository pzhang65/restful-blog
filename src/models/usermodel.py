# src/models/usermodel.py
from marshmallow import fields, Schema
from pytz import timezone
import datetime
from . import db
from . import db, bcrypt

class UserModel(db.Model):
    #EST timezone class attribute
    tz = timezone('EST')

    # table name
    __tablename__ = 'users'

    # declaring column names
    id = db.Column(db.Integer, primary_key=True) #id primary key
    # request will return none when returning that object doesn't exist
    name = db.Column(db.String(128), nullable=False) # nullable false something must be returned from POST
    #Candiate key but not chosen as primary therefore alternate key!
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password')) # hash user password before storing to db
        self.created_at = datetime.datetime.now(self.tz)
        self.modified_at = datetime.datetime.now(self.tz)


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password': # if users wants to update password
                self.password = self.__generate_hash(value) # hash new password
            setattr(self, key, item)
        self.modified_at = datetime.now(tz)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
    All actual SQL queries are converted by SQLAlchemy, intialized in __init__.py
    """

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    # private method to hash user password for storage in db
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)


    def __repr__(self):
        return f'<id {self.id}>'


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)

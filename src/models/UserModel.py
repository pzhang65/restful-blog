# src/models/UserModel.py
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
    # nullable means something must be returned from POST
    # request will return none when returning that object doesn't exist
    name = db.Column(db.String(128), nullable=False)
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
        self.created_at = datetime.now(tz)
        self.modified_at = datetime.now(tz)


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

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

    # private method to hash user password for storage in db
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    # add this new method
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)


    def __repr__(self):
        return f'<id {self.id}>'

    def __str__(self):
        return f'User name: {self.name}, user ID: {self.id}, email: {user.email}'

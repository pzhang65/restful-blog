# src/models/blogpostmodel.py
from marshmallow import fields, Schema
from pytz import timezone
import datetime
from . import db
from . import db, bcrypt

class BlogpostModel(db.Model):
    __tablename__ = 'blogposts'
    tz = timezone('EST')

    # declaring column names
    id = db.Column(db.Integer, primary_key=True) #id primary key
    # request will return none when returning that object doesn't exist
    title = db.Column(db.String(128), nullable=False) # nullable false something must be returned from POST
    contents = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.title = data.get('title')
        self.contents = data.get('contents')
        self.owner_id = data.get('owner_id')
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
    def get_all_blogposts():
        return BlogpostModel.query.all()

    @staticmethod
    def get_one_blogpost(id):
        return BlogpostModel.query.get(id)

    @staticmethod
    def get_user_blogposts(id):
        return BlogpostModel.query.get(owner_id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class BlogpostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    contents = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)

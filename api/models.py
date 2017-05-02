"""API version 1.0 models.

api/models.py
"""
import jwt
import datetime
from marshmallow import Schema, fields, pre_load
from marshmallow import validate, validates_schema, ValidationError
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from api import db


ma = Marshmallow()


class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()
    
    def update(self):
        return db.session.commit()
    
    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class User(db.Model, AddUpdateDelete):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    bucketlists = db.relationship('BucketList', backref='user', lazy=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user_id):
        """
        :param user_id:
        :return: string
        """
        try:
            payload = {
                # expiration period
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=600),
                # time of creation of the token
                'iat': datetime.datetime.utcnow(),
                # subject of the token
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as error:
            return error
    
    @staticmethod
    def decode_auth_token(auth_token):
        """"
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Session has expired. Login to get a new token'
        except jwt.InvalidTokenError:
            return 'Invalid token.'
    
    
class BucketList(db.Model, AddUpdateDelete):
    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime)
    items = db.relationship('BucketItem', backref='bucketlist', lazy=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<BucketList %r>' % self.name


class BucketItem(db.Model, AddUpdateDelete):
    __tablename__ = 'bucketitem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    date_closed = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'), nullable=False)

    def __repr__(self):
        return '<BucketItem %r>' % self.name
    
    
# Schemas do validate, serialize and deserialize models
# consider adding urls
class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(validate=(validate.Length(min=1, error='Username Required')))
    password = fields.String(validate=validate.Length(min=1, error='Password Required'))
    email = fields.String(validate=(validate.Length(min=1, error='Email Required'),
                                    validate.Email(error='{input} :Invalid Email address')))
    created_date = fields.DateTime()
    bucketlists = fields.Nested('BucketListSchema', many=True, exclude=('user'))
    
 
class BucketListSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=validate.Length(min=1, error='Bucketlist Name Required'))
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    user = fields.Nested('UserSchema', only=['id', 'username'])
    items = fields.Nested('BucketItemSchema', many=True, exclude=('bucketlist',))
    url = ma.URLFor('api_v1.bucketlist', id='<bucket_id>', _external=True)
    
    
class BucketItemSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=validate.Length(min=1, error='Bucketitem Name Required'))
    done = fields.Boolean(default=False)
    date_created = fields.DateTime()
    date_closed = fields.DateTime()
    date_modified = fields.DateTime()
    bucketlist = fields.Nested('BucketListSchema', only=['id', 'name'],
                               required=True)
    url = ma.URLFor('api_v1.bucketlistitem', id='<item_id>', _external=True)

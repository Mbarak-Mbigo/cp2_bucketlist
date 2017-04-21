"""API version 1.0 models.

api/models.py
"""
from datetime import datetime
from api import db


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
    password = db.Column(db.String)
    email = db.Column(db.String(150), unique=True, nullable=False)
    bucketlists = db.relationship('BucketList', backref='user', lazy=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username


class BucketList(db.Model, AddUpdateDelete):
    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
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
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_closed = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'), nullable=False)

    def __repr__(self):
        return '<BucketItem %r>' % self.name

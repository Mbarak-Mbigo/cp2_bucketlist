"""API version 1.0 models."""
from datetime import datetime
from api import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username


class BucketList(db.Model):
    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(30), default='created')
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    accomplished_date = db.Column(db.DateTime)
    closed_date = db.Column(db.DateTime)
    open_duration = db.Column(db.Integer)
    items = db.relationship('BucketItem', backref='bucketlist', lazy=True)

    def __repr__(self):
        return '<BucketList %r>' % self.name


class BucketItem(db.Model):
    __tablename__ = 'bucketitem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    accomplished_date = db.Column(db.DateTime)
    closed_date = db.Column(db.DateTime)
    open_duration = db.Column(db.Integer)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'),
                          nullable=False)

    def __repr__(self):
        return '<BucketItem %r>' % self.name

# api/schemas.py

from marshmallow import Schema, fields, pre_load
from marshmallow import validate, validates_schema, ValidationError
from flask_marshmallow import Marshmallow

ma = Marshmallow()


# Schemas do validate, serialize and deserialize models
class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(validate=(validate.Length(min=1, error='Username Required')))
    password = fields.String(validate=validate.Length(min=1, error='Password Required'))
    email = fields.String(validate=(validate.Length(min=1, error='Email Required'),
                                    validate.Email(error='Invalid Email address')))
    created_date = fields.DateTime()


class BucketListSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=validate.Length(min=1, error='Bucketlist Name Required'))
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    user = fields.Nested('UserSchema', only=['id', 'username'])
    items = fields.Nested('BucketItemSchema', many=True, exclude=('bucketlist',))
    url = ma.UrlFor('api_v1.bucket_list', id='<id>', _external=True)


class BucketItemSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=validate.Length(min=1, error='Bucketitem Name Required'))
    done = fields.Boolean(default=False)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    bucketlist = fields.Nested('BucketListSchema', only=['id', 'name'])
    url = ma.UrlFor('api_v1.bucket_item', id='<bucket_id>', item_id='<id>', _external=True)

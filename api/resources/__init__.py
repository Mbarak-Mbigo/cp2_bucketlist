# api/resources/__init__.py
from flask import Blueprint
from flask_restful import Api

from api.resources.bucketlist import BucketList
# arguments: blueprint name and a module/package where the blueprint is located
api_v1 = Blueprint('api_v1', __name__)

api = Api(api_v1)

# Endpoints
# public access : True
api.add_resource(BucketList, '/auth/login', endpoint='auth')
api.add_resource(BucketList, '/auth/register', endpoint='auth_register')

# public access : False
api.add_resource(BucketList, '/bucketlists/', endpoint='bucket_lists')
api.add_resource(BucketList, '/bucketlists/<id>', endpoint='bucket_list')
api.add_resource(BucketList, '/bucketlists/<id>/items/', endpoint='bucket_items')
api.add_resource(BucketList, '/bucketlists/<id>/items/<item_id>', endpoint='bucket_item')


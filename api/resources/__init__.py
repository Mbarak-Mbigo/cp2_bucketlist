# api/resources/__init__.py
from flask import Blueprint
from flask_restful import Api

from api.resources.bucketlist import BucketList, BucketLists, BucketItem, BucketItems
# arguments: blueprint name and a module/package where the blueprint is located
api_v1 = Blueprint('api_v1', __name__)

api = Api(api_v1)

# public access : False
api.add_resource(BucketLists, '/bucketlists/', endpoint='bucket_lists')
api.add_resource(BucketList, '/bucketlists/<int:id>', endpoint='bucket_list')
api.add_resource(BucketItems, '/bucketlists/<int:id>/items/', endpoint='bucket_items')
api.add_resource(BucketItem, '/bucketlists/<int:id>/items/<int:item_id>', endpoint='bucket_item')


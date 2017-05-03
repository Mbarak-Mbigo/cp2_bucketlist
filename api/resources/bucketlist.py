# api/resources/bucketlist.py
from flask import request, jsonify, g, make_response
from sqlalchemy.exc import SQLAlchemyError

from common.authentication import AuthRequiredResource
from api.models import User, BucketList, BucketItem, BucketItemSchema, BucketListSchema, db

buckets_schema = BucketListSchema()


class ResourceBucketLists(AuthRequiredResource):
    # get all bucketlists for the user
    def get(self):
        buckets_query = BucketList.query.filter_by(created_by=g.user.id)
        buckets = buckets_schema.dump(buckets_query, many=True).data
        return buckets, 200
    
    # create a bucketlist for the user
    def post(self):
        request_data = request.get_json()
        if not request_data:
            response = {'Bucketlist': 'No input data provided'}
            return response, 400
        errors = buckets_schema.validate(request_data)
        if errors:
            return errors, 403
        try:
            bucket_name = request_data['name']
            exists = BucketList.query.filter_by(name=bucket_name).first()
            if not exists:
                bucketlist = BucketList()
                bucketlist.name = bucket_name
                bucketlist.created_by = g.user.id
                bucketlist.add(bucketlist)
                
                response_data = BucketList.query.filter_by(name=bucket_name).first()
                response = buckets_schema.dump(response_data).data
                return response, 201
            else:
                response = {
                    'Error': '{} already exists!'.format(bucket_name)
                }
                return response, 409
        except SQLAlchemyError as error:
            db.session.rollback()
            response = {'error': str(error)}
            return response, 401


class ResourceBucketList(AuthRequiredResource):
    def get(self, id):
        # return all bucketlists with their items for the user
        # return a specific bucketlist with its items for the user
        bucket = BucketList.query.get_or_404(id)
        response = buckets_schema.dump(bucket).data
        print(response)
        return response
    
    def put(self, bucket_id):
        # edit a bucketlist
        pass
    
    def delete(self, bucket_id):
        # delete a bucketlist
        pass
    

class ResourceBucketItems(AuthRequiredResource):
    # create a new item, in bucketlist
    def post(self, bucket_id):
        pass
    
    # get all bucket items
    def get(self, bucket_id):
        pass
    
      
class ResourceBucketItem(AuthRequiredResource):
    # get a single bucket item
    def get(self, item_id):
        pass
    
    def put(self, item_id):
        # Update a bucket list item
        pass
    
    def delete(self, item_id):
        # Delete a bucketlist item
        pass

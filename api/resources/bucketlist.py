# api/resources/bucketlist.py
import datetime

from flask import request, jsonify, g, make_response
from sqlalchemy.exc import SQLAlchemyError

from common.authentication import AuthRequiredResource
from api.models import User, BucketList, BucketItem, BucketItemSchema, BucketListSchema, db

buckets_schema = BucketListSchema()
bucketitem_schema = BucketItemSchema()


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
        return response, 200
    
    def put(self, id):
        # edit a bucketlist
        bucket = BucketList.query.get_or_404(id)
        bucket_request = request.get_json(force=True)
        if 'name' in bucket_request:
            bucket.name = bucket_request['name']
            bucket.date_modified = datetime.datetime.now()
        dumped_message, dump_errors = buckets_schema.dump(bucket)
        if dump_errors:
            return dump_errors, 400
        validate_error = buckets_schema.validate(dumped_message)
        if validate_error:
            return validate_error, 400
        try:
            bucket.update()
            return self.get(id)
        except SQLAlchemyError as error:
            db.session.rollback()
            response = jsonify({"error": str(error)})
            return response, 400
        
    def delete(self, id):
        # delete a bucketlist
        bucket = BucketList.query.get_or_404(id)
        try:
            bucket.delete(bucket)
            response = {
                'Status': 'Delete operation successful'
            }
            return response, 204
        except SQLAlchemyError as error:
            db.session.rollback()
            response = jsonify({"error": str(error)})
            return response, 401
    

class ResourceBucketItems(AuthRequiredResource):
    # create a new item, in bucketlist
    def post(self, id):
        request_data = request.get_json()
        if not request_data:
            response = {
                'Error': 'No input data not provided'
            }
            return response, 400
        errors = bucketitem_schema.validate(request_data)
        if errors:
            return errors, 403
        try:
            bucket_item_name = request_data['name']
            exists = BucketItem.query.filter_by(name=bucket_item_name).first()
            if not exists:
                bucket_item = BucketItem()
                bucket_item.name = request_data['name']
                bucket_item.bucket_id = id
                bucket_item.add(bucket_item)
                
                response_data = BucketItem.query.filter_by(name=bucket_item_name).first()
                response = bucketitem_schema.dump(response_data).data
                return response, 201
            else:
                response = {
                    'Error': '{} already exists!'.format(bucket_item_name)
                }
                return response, 409

        except SQLAlchemyError as error:
            db.session.rollback()
            response = {'error': str(error)}
            return response, 401

    # get all bucket items
    def get(self, id):
        bucket_items_query = BucketItem.query.filter_by(bucket_id=id)
        bucketitems = bucketitem_schema.dump(bucket_items_query, many=True).data
        return bucketitems, 200
    
      
class ResourceBucketItem(AuthRequiredResource):
    # get a single bucket item
    def get(self, id, item_id):
        bucket = BucketItem.query.get_or_404(item_id)
        response = bucketitem_schema.dump(bucket).data
        return response, 200
    
    def put(self, id, item_id):
        # Update a bucket list item
        bucket_item = BucketItem.query.get_or_404(item_id)
        bucket_item_request = request.get_json(force=True)
        if not bucket_item_request:
            response = {
                'Error': 'Nothing to update'
            }
            return response, 412
        else:
            if 'name' in bucket_item_request:
                bucket_item.name = bucket_item_request['name']
            if 'done' in bucket_item_request:
                bucket_item.done = bucket_item_request['done']
            if 'done' in bucket_item_request and bucket_item_request['done']:
                bucket_item.date_closed = datetime.datetime.now()
                
            bucket_item.date_modified = datetime.datetime.now()
        dumped_message, dump_errors = bucketitem_schema.dump(bucket_item)
        if dump_errors:
            return dump_errors, 400
        validate_error = bucketitem_schema.validate(dumped_message)
        if validate_error:
            print('Am here validate error: {}'.format(validate_error))
            return validate_error, 400
        try:
            bucket_item.update()
            return self.get(item_id)
        except SQLAlchemyError as error:
            db.session.rollback()
            response = jsonify({"error": str(error)})
            return response, 400
    
    def delete(self, id, item_id):
        # Delete a bucketlist item
        bucket_item = BucketItem.query.get_or_404(item_id)
        try:
            bucket_item.delete(bucket_item)
            response = {
                'Status': 'Delete operation successful'
            }
            return response, 204
        except SQLAlchemyError as error:
            db.session.rollback()
            response = jsonify({"error": str(error)})
            return response, 401

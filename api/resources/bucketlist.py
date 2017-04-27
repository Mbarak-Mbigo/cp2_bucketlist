# api/resources/bucketlist.py
from flask_restful import Resource


class BucketList(Resource):
    def get(self, id=None):
        # return all bucketlists with their items for the user
        # return a specific bucketlist with its items for the user
        pass
    
    def post(self):
        # create a bucketlist
        pass
    
    def put(self, id):
        # edit a bucketlist
        pass
    
    def delete(self, id):
        # delete a bucketlist
        pass
    
    
class BucketItem(Resource):
    # Create a new item in bucket list
    def post(self):
        pass
    
    def put(self, id):
        # Update a bucket list item
        pass
    
    def delete(self, id):
        # Delete a bucketlist item
        pass

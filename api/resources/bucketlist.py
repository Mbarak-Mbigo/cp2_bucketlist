from flask_restful import Resource


class Bucketlist(Resource):
    def get(self):
        # return all bucketlists with their items for the user
        pass
    
    def get(self, id):
        # return bucketlist with its items for the user
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

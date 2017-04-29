# api/resources/bucketlist.py
from common.authentication import AuthRequiredResource
    

class BucketLists(AuthRequiredResource):
    # get all bucketlists for the user
    def get(self, user_id):
        pass
    
    # create a bucketlist for the user
    def post(self, user_id):
        pass


class BucketList(AuthRequiredResource):
    def get(self, bucket_id):
        # return all bucketlists with their items for the user
        # return a specific bucketlist with its items for the user
        pass
    
    def put(self, bucket_id):
        # edit a bucketlist
        pass
    
    def delete(self, bucket_id):
        # delete a bucketlist
        pass
    

class BucketItems(AuthRequiredResource):
    # create a new item, in bucketlist
    def post(self, bucket_id):
        pass
    
    # get all bucket items
    def get(self, bucket_id):
        pass
    
      
class BucketItem(AuthRequiredResource):
    # get a single bucket item
    def get(self, item_id):
        pass
    
    def put(self, item_id):
        # Update a bucket list item
        pass
    
    def delete(self, item_id):
        # Delete a bucketlist item
        pass

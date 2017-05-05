# api/tests/test_resource_bucketlist.py

import json

from api.tests.base_case import BucketBaseCase

new_bucketlist = {
    'name': 'Bucketlist_1',
    'description': 'Social interactions',
}

update_bucket_list = {
    'name': 'My_Bucketlist_1'
}

new_bucket_item = {
    'name' : "Visit a children's home"
}

invalid_token = {
    'auth_token': 'akdfjafiqowerijqdfjwfj.qoifjdifjfwejqfdjfdjfqojfdjdjf.qwejdjcajqwesdadkasfafasdfafdsfdf'
}


class TestBucketlist(BucketBaseCase):
    def test_create_bucketlist_with_a_valid_token(self):
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps(new_bucketlist)
        )
        self.assertEqual(response.status_code, 201)
        
    def test_create_bucketlist_with_invalid_token(self):
        auth_headers = self.get_authentication_content_type_headers()
        auth_headers['Authorization'] = 'Bearer' + invalid_token['auth_token']
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=auth_headers,
            data=json.dumps(new_bucketlist)
        )
        self.assertTrue(response.status_code==401)
        
    def test_retrieve_bucketlists(self):
        response = self.test_client.get(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers()
        )
        self.assertEqual(response.status_code, 200)
    
    def test_retrieving_bucketlists_with_invalid_token(self):
        auth_headers = self.get_authentication_content_type_headers()
        auth_headers['Authorization'] = 'Bearer' + invalid_token['auth_token']
        response = self.test_client.get(
            '/api/v1/bucketlists/',
            headers=auth_headers,
        )
        self.assertTrue(response.status_code==401)
    
    def test_retrieving_a_non_existent_bucketlist(self):
        response = self.test_client.get(
            '/api/v1/bucketlists/150',
            headers=self.get_authentication_content_type_headers()
        )
        self.assertEqual(response.status_code, 404)
    
    def test_updating_a_non_existent_bucketlist(self):
        response = self.test_client.put(
            '/api/v1/bucketlists/150',
            headers=self.get_authentication_content_type_headers()
        )
        self.assertEqual(response.status_code, 404)
        
    # def test_updating_a_bucketlist_with_valid_details(self):
    #     pass
    #
    # def test_results_are_paginated(self):
    #     pass
    #
    # def test_allows_searching_by_name(self):
    #     pass
    #
    # def test_searching_a_non_existent_resource(self):
    #     pass

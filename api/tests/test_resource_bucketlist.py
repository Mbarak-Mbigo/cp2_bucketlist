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
        auth_headers['Authorization'] = invalid_token['auth_token']
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
        auth_headers['Authorization'] = invalid_token['auth_token']
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
        
    def test_updating_a_bucketlist_with_valid_details(self):
        pass
    # # Invalid token
    # def test_create_bucketlist_with_invalid_token(self):
    #     token_auth_headers = self.get_accept_content_type_headers()
    #     token_auth_headers['Authorization'] = invalid_token['auth_token']
    #
    #     new_bucketlist['created_by'] = 'user_01'
    #     create_bucketlist_response = self.test_client.post(
    #         '/api/v1/bucketlists',
    #         headers=token_auth_headers,
    #         data=json.dumps(new_bucketlist)
    #     )
    #
    #     self.assertEqual(create_bucketlist_response.status_code, 401)
    #
    # def test_create_bucketlist_with_valid_credentials(self):
    #     # register user
    #     register_response = self.register_user('user_01', '@1.618user_01', 'user_01@gmail.com')
    #     self.assertEqual(register_response.status_code, 201)
    #
    #     token_auth_headers = self.get_accept_content_type_headers()
    #     token_auth_headers['Authorization'] = register_response['auth_token']
    #
    #     new_bucketlist['created_by'] = register_response['username']
    #     create_bucketlist_response = self.test_client.post(
    #         '/api/v1/bucketlists',
    #         headers=token_auth_headers,
    #         data=json.dumps(new_bucketlist)
    #     )
    #
    #     self.assertEqual(create_bucketlist_response.status_code, 201)
    #
    #
    #
    #
    #
    #
    #
    #
    # def test_retrieve_bucketlist_with_invalid_credentials(self):
    #     response = self.test_client.get(
    #         '/api/v1/bucketlists/',
    #         headers=self.get_authentication_headers(user_with_invalid_credentials['token'], ''),
    #         data=json.dumps(new_bucketlist))
    #     self.assertEqual(response.status_code, 401)
    #
    #
    # def test_retrieve_bucketlist_with_credentials(self):
    #     response = self.test_client.get(
    #         '/api/v1/bucketlists/',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''),
    #         data=json.dumps(new_bucketlist))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_upating_bucketlist_with_invalid_credentials(self):
    #     response = self.test_client.put(
    #         '/api/v1/bucketlists/1',
    #         headers=self.get_authentication_headers(user_with_invalid_credentials['token'], ''),
    #         data=json.dumps(update_bucket_list))
    #     self.assertEqual(response.status_code, 401)
    #
    # def test_updating_bucketlist_with_valid_credentials(self):
    #     response = self.test_client.put(
    #         '/api/v1/bucketlists/1',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''),
    #         data=json.dumps(update_bucket_list))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_deleting_an_existing_bucketlist(self):
    #     response = self.test_client.delete(
    #         '/api/v1/bucketlists/1',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''),
    #         data=json.dumps(update_bucket_list))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_deleting_a_non_existent_bucketlist(self):
    #     response = self.test_client.delete(
    #         '/api/v1/bucketlists/1000',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''),
    #         data=json.dumps(update_bucket_list))
    #     self.assertEqual(response.status_code, 404)
    #
    # def test_updating_non_existent_bucketlist(self):
    #     response = self.test_client.put(
    #         '/api/v1/bucketlists/1000',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''),
    #         data=json.dumps(update_bucket_list))
    #     self.assertEqual(response.status_code, 404)
    #
    # def test_creating_bucketitem_in_an_existing_bucketlist(self):
    #     response = self.test_client.post(
    #         '/api/v1/bucketlists/1/items/',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''),
    #         data=json.dumps(new_bucket_item))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_retrieving_bucketitems_in_an_existing_bucketlist(self):
    #     response = self.test_client.get(
    #         '/api/v1/bucketlists/1/items/',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_updating_an_existing_bucketitem(self):
    #     response = self.test_client.put(
    #         '/api/v1/bucketlists/1/items/1',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_updating_a_non_existent_bucketitem(self):
    #     response = self.test_client.put(
    #         '/api/v1/bucketlists/1/items/150',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''))
    #     self.assertEqual(response.status_code, 404)
    #
    # def test_deleting_an_existing_bucketitem(self):
    #     response = self.test_client.delete(
    #         '/api/v1/bucketlists/1/items/2',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_deleting_a_non_existent_bucketitem(self):
    #     response = self.test_client.delete(
    #         '/api/v1/bucketlists/1/items/2',
    #         headers=self.get_authentication_headers(user_with_valid_credentials['token'], ''))
    #     self.assertEqual(response.status_code, 404)

    def test_results_are_paginated(self):
        pass

    def test_allows_searching_by_name(self):
        pass

    def test_searching_a_non_existent_resource(self):
        pass

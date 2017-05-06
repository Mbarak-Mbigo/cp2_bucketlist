# api/tests/test_resource_bucketlist.py

import json
from flask import current_app

from api.tests.base_case import BucketBaseCase

new_bucketlist = {
    'name': 'Bucketlist_1'
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
        # Getting bucketlists when none is created
        response = self.test_client.get(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers()
        )
        self.assertEqual(response.status_code, 404)
        # create bucketlists
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Remember the Old'
            })
        )
        self.assertTrue(response.status_code == 201)
        # create another bucketlist
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Give Zakat'
            })
        )
        self.assertTrue(response.status_code == 201)
        # Retrieve created bucket lists bucketlists
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
        
    def test_updating_a_bucketlist_with_valid_details(self):
        # create a bucketlist
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data = json.dumps({
                'name': 'Fulfil dreams'
            })
        )
        self.assertTrue(response.status_code==201)
        # update created bucketlist
        created_object = json.loads(response.data.decode())
        response = self.test_client.put(
            created_object['url'],
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Fulfil Swimming dream'
            })
        )
        self.assertEqual(response.status_code,200)

    def test_results_are_paginated(self):
        # create bucketlist 1
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Travelling'
            })
        )
        self.assertTrue(response.status_code == 201)
        # create bucketlist 2
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Social life'
            })
        )
        self.assertTrue(response.status_code == 201)
        # create bucketlist 3
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Cultivate saving culture'
            })
        )
        self.assertTrue(response.status_code == 201)
        # create bucketlist 4
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Build a car'
            })
        )
        self.assertTrue(response.status_code == 201)
        # create bucketlist 5
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Start a business venture'
            })
        )
        self.assertTrue(response.status_code == 201)
        # create bucketlist 6
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Visit Mida'
            })
        )
        self.assertTrue(response.status_code == 201)
        # create bucketlist 7
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Divide my Wealth'
            })
        )
        self.assertTrue(response.status_code == 201)
        # Retrieve the first 5
        response = self.test_client.get(
            '/api/v1/bucketlists/?limit=5',
            headers=self.get_authentication_content_type_headers()
        )
        self.assertEqual(response.status_code, 200)
        paginated_results = json.loads(response.data.decode())
        # Check buckets on page 1 are 5
        self.assertEqual(len(paginated_results['results']), 5)
        # Check total count is 7 (number of objects created)
        self.assertEqual(paginated_results['count'], 7)
        # Checkt default page size is 20
        self.assertEqual(current_app.config['DEFAULT_PAGINATION_PAGE_SIZE'], 20)

    def test_allows_searching_by_name(self):
        # create bucketlist
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Travelling'
            })
        )
        self.assertTrue(response.status_code == 201)
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Social life'
            })
        )
        self.assertTrue(response.status_code == 201)
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Cultivate saving culture'
            })
        )
        self.assertTrue(response.status_code == 201)
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Build a car'
            })
        )
        self.assertTrue(response.status_code == 201)
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Start a business venture'
            })
        )
        self.assertTrue(response.status_code == 201)
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Visit Mida'
            })
        )
        self.assertTrue(response.status_code == 201)
        response = self.test_client.post(
            '/api/v1/bucketlists/',
            headers=self.get_authentication_content_type_headers(),
            data=json.dumps({
                'name': 'Divide my Wealth'
            })
        )
        self.assertTrue(response.status_code == 201)
        response = self.test_client.get(
            '/api/v1/bucketlists/?q=ing',
            headers=self.get_authentication_content_type_headers()
        )
        search_results = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        # Check only two bucketlists match search term (Travelling and Cultivate saving Culture)
        self.assertEqual(search_results['count'], 2)
        # Check results for a search with no match
        response = self.test_client.get(
            '/api/v1/bucketlists/?q=3433',
            headers=self.get_authentication_content_type_headers()
        )
        search_results = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)

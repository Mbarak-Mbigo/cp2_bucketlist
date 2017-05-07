# api/tests/base_case.py
import os.path
import unittest
import json

from api import create_app, db
from api.models import User

bucketlists_data = [
    'Swimming',
    'Reading',
    'Travelling',
    'Philanthropy',
    'Reading',
    'Spiritual Enlightment',
    'Open Source Contribution',
    'Charity',
    'Get Married',
    'Motivational Speaking',
    'Teaching',
    'Face my Fears',
    'Conquer my Fears',
    'Start Blogging',
    'Learn a new language',
    'Travel abroad',
    'Hijjah',
    'Own a home',
    'Build a bot',
    'Racing',
    'Invest in shares',
    'Stop betting',
    'Adopt a child',
    'Sponsor a needy student',
    'Build Social Profile',
    'Riding bikes',
    'Own a Rolls Royce',
    'Meet Bill Gates',
    'Own a Park',
    'Learn Martial Arts',
    'Go Deep Sea Fishing',
    'Learn Salsa'
]


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # test user details
        self.test_username = 'test_user_00'
        self.test_password = '@test_usr_pwd#'
        self.test_email = 'user_00@gmail.com'
        # create default test user
        self.test_user = User()
        self.test_user.username = self.test_username
        self.test_user.password = self.test_password
        self.test_user.email = self.test_email
        self.test_user.add(self.test_user)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def get_accept_content_type_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
  
    
class BucketBaseCase(BaseTestCase):
    def login_default_user(self):
        login_response = self.test_client.post(
            '/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps({
                'username': self.test_username,
                'password': self.test_password
            })
        )
        login_resp_data = json.loads(login_response.data.decode())
        return login_resp_data
    
    def get_authentication_content_type_headers(self):
        authentication_headers = self.get_accept_content_type_headers()
        token = self.login_default_user()['token']
        authentication_headers['Authorization'] = 'Bearer ' + token
        return authentication_headers
    
    def create_bucketlists_using_dummy_data(self, bucketlist_data):
        response = None
        for bucket_name in bucketlist_data:
            response = self.test_client.post(
                '/api/v1/bucketlists/',
                headers=self.get_authentication_content_type_headers(),
                data=json.dumps({
                    'name': bucket_name
                })
            )
        return response
    
    def create_bucketlist_items_using_dummy_data(self, data_file):
        pass

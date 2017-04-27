# api/tests/base_case.py
import unittest
import json
from api import create_app, db
from api.models import User


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
    
    def register_user(self, username, password, email):
        response = self.test_client.post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps({
                'username': username,
                'password': password,
                'email': email
            })
        )
        return response

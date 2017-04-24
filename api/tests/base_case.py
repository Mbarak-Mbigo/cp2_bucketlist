import unittest
from base64 import b64encode

from flask import current_app
from api import create_app, db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def get_accept_content_type_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_authentication_headers(self, username,password):
        authentication_headers = self.get_accept_content_type_headers()
        authentication_headers['Authorization'] = \
            'Basic ' + b64encode((username + ':' + password).encode('utf- 8')).decode('utf-8')
        return authentication_headers

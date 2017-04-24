# api/tests/test_resource_user.py
import json

from api.tests.base_case import BaseTestCase

new_user = {
    'username': 'Rayyah Timamy',
    'password': '@1324Tibim',
    'email': 'rayyah@gmail.com'
}

new_user_no_username = {
    'username': '',
    'password': '@1324Tibim',
    'email': 'rayyah@gmail.com'
}

new_user_no_password = {
    'username': 'Rayyah Timamy',
    'password': '',
    'email': 'rayyah@gmail.com'
}

new_user_invalid_email = {
    'username': 'Rayyah Timamy',
    'password': '@1324Tibim',
    'email': 'rayyahgmail.com'
}

new_user_duplicate = {
    'username': 'Rayyah Timamy',
    'password': '@1324Tibim',
    'email': 'rayyah@gmail.com'
}


class TestUserRegistration(BaseTestCase):

    def test_register_new_user(self):
        response = self.test_client.post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(new_user))
        self.assertEqual(response.status_code, 201)
        
    def test_register_user_with_no_username(self):
        response = self.test_client.post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(new_user_no_username))
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Invalid username or password', json.loads(response.data))
        
    def test_register_user_with_no_password(self):
        response = self.test_client.post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(new_user_no_password))
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Invalid username or password', json.loads(response.data))

    def test_register_user_with_invalid_email(self):
        response = self.test_client.post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(new_user_invalid_email))
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Invalid email', json.loads(response.data))
        
    def test_register_user_with_duplicate_details(self):
        response = self.test_client.post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(new_user_duplicate))
        self.assertEqual(response.status_code, 409)
        self.assertTrue('User already exists!', json.loads(response.data))

new_user_02 = {
    'username': 'user_02',
    'password': '@user!pwd#',
    'email': 'user02@gmail.com'
}

user_login_password = {
    'username': 'user_01',
    'password': '@user!pwd#'
}

user_login_invalid_username = {
    'username': 'user_00',
    'password': '@user!pwd#'
}

user_login_invalid_password = {
    'username': 'user_01',
    'password': '@user'
}

user_access_invalid_token = {
    'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzgyJpZCI6MX0.',
    'username': 'user_02'
}


class TestUserLogin(BaseTestCase):
    def test_register_new_user(self):
        response = self.test_client.post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(new_user_02))
        self.assertEqual(response.status_code, 201)
    
    def test_token_authentication(self):
        # login
        response = self.test_client.get(
            '/auth/login',
            data=json.dumps(new_user_02))
        self.assertEqual(response.status_code, 202)
    
        # request access token
        response = self.test_client.get(
            '/auth/token',
            token=json.dumps(new_user_02))
        self.token = token
        self.assertEqual(response.status_code, 200)
        # use access token
        use_user_token = {
            'token': self.token,
            'username': 'user_02'
        }
        response = self.test_client.get(
            '/api/v1/bucketlist/',
            data=json.dumps(use_user_token))
        self.assertEqual(response.status_code, 200)
        
        # use invalid access token
        response = self.test_client.get(
            '/api/v1/bucketlist/',
            data=json.dumps(user_access_invalid_token))
        self.assertEqual(response.status_code, 200)
        
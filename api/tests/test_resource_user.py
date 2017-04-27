# api/tests/test_resource_user.py
import json

from api.tests.base_case import BaseTestCase

user_no_username = {
    'username': '',
    'password': '@user01!pwd#',
    'email': 'user01@gmail.com'
}

user_no_password = {
    'username': 'user_01',
    'password': '',
    'email': 'user01@gmail.com'
}

user_no_email = {
    'username': 'user_01',
    'password': '@user01!pwd#',
    'email': ''
}

user_malformed_email = {
    'username': 'user_01',
    'password': '@user01!pwd#',
    'email': 'user01gmail.com'
}

user_correct_credentials = {
    'username': 'user_01',
    'password': '@user01!pwd#',
    'email': 'user01@gmail.com'
}


class TestUserRegistration(BaseTestCase):
    def test_register_user_with_no_username(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_no_username)
        )
        self.assertEqual(register_response.data,'Username required')
        self.assertEqual(register_response.status_code, 400)
    
    def test_register_user_with_no_password(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_no_password)
        )
        self.assertEqual(register_response.data, 'Password required')
        self.assertEqual(register_response.status_code, 400)
        
    def test_register_user_with_no_email(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_no_email)
        )
        self.assertEqual(register_response.data, 'Email required')
        self.assertEqual(register_response.status_code, 400)
        
    def test_register_user_with_malformed_email(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_no_email)
        )
        self.assertEqual(register_response.data, 'Invalid email')
        self.assertEqual(register_response.status_code, 403)
        
    def test_register_user_with_correct_details(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_correct_credentials)
        )
        self.assertEqual(register_response.status_code, 201)
        
    def test_register_existing_user(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_correct_credentials)
        )
        self.assertEqual(register_response.data, 'User already exist!')
        self.assertEqual(register_response.status_code, 409)


class TestUserLogin(BaseTestCase):
    def test_login_user_with_correct_credentials_works(self):
        login_response = self.test_client.post(
            '/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps({
                'username': self.test_username,
                'password': self.test_password
            }
            )
        )
        self.assertEqual(login_response.status_code, 200)
        
    def test_login_user_with_no_username(self):
        login_response = self.test_client.post(
            '/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps({
                'username': '',
                'password': self.test_password
            }
            )
        )
        self.assertEqual(login_response.data, 'Provide username')
        self.assertEqual(login_response.status_code, 400)
        
    def test_login_user_with_no_password(self):
        login_response = self.test_client.post(
            '/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps({
                'username': self.test_username,
                'password': ''
            }
            )
        )
        self.assertEqual(login_response.data, 'Provide password')
        self.assertEqual(login_response.status_code, 40)
        
    def test_login_user_with_incorrect_username(self):
        login_response = self.test_client.post(
            '/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps({
                'username': 'incorrect_username',
                'password': self.test_password
            }
            )
        )
        self.assertEqual(login_response.data, 'Invalid username or password')
        self.assertEqual(login_response.status_code, 401)
        
    def test_login_user_with_incorrect_password(self):
        login_response = self.test_client.post(
            '/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps({
                'username': self.test_username,
                'password': 'incorrect_pwd'
            }
            )
        )
        self.assertEqual(login_response.data, 'Invalid username or password')
        self.assertEqual(login_response.status_code, 401)

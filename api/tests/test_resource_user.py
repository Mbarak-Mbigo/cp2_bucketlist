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
        data = json.loads(register_response.data.decode())
        self.assertEqual(data['username'][0],'Username Required')
        self.assertEqual(register_response.status_code, 403)
    
    def test_register_user_with_no_password(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_no_password)
        )
        data = json.loads(register_response.data.decode())
        self.assertEqual(data['password'][0], 'Password Required')
        self.assertEqual(register_response.status_code, 403)
        
    def test_register_user_with_no_email(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_no_email)
        )
        data = json.loads(register_response.data.decode())
        self.assertEqual(data['email'][0], 'Email Required')
        self.assertEqual(register_response.status_code, 403)
        
    def test_register_user_with_malformed_email(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_malformed_email)
        )
        data = json.loads(register_response.data.decode())
        self.assertEqual(data['email'][0], 'Invalid Email address')
        self.assertEqual(register_response.status_code, 403)
        
    def test_register_user_with_correct_details(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_correct_credentials)
        )
        response_data = json.loads(register_response.data.decode())
        self.assertEqual(register_response.status_code, 201)
        # check token available
        self.assertTrue(response_data['token'])
        
    def test_register_existing_user(self):
        register_response = self.test_client.post(
            'auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps({
                'username': self.test_username,
                'password': self.test_password
            })
        )
        data = json.loads(register_response.data.decode())
        self.assertEqual(data['Error'], 'User {} already exists!'.format(self.test_username))
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
        login_data = json.loads(login_response.data.decode())
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(login_data['token'])
        
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
        data = json.loads(login_response.data.decode())
        self.assertEqual(data['Error'], 'Invalid username or password')
        self.assertEqual(login_response.status_code, 401)
        
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
        data = json.loads(login_response.data.decode())
        self.assertEqual(data['Error'], 'Invalid username or password')
        self.assertEqual(login_response.status_code, 401)
        
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
        data = json.loads(login_response.data.decode())
        self.assertEqual(data['Error'], 'Invalid username or password')
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
        data = json.loads(login_response.data.decode())
        self.assertEqual(data['Error'], 'Invalid username or password')
        self.assertEqual(login_response.status_code, 401)

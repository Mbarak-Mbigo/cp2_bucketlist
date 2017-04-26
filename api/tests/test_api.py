# api/tests/test_api.py

import json

from flask import current_app

from api.tests.base_case import BaseTestCase


class TestApi(BaseTestCase):

    def test_app_in_testing_configurations(self):
        self.assertFalse(current_app is None)
        self.assertTrue(current_app.config['TESTING'])
        self.assertTrue(current_app.config['DEBUG'])
        self.assertEqual(
            current_app.config['SQLALCHEMY_DATABASE_URI'], 'postgresql://db_admin: @127.0.0.1/bucketlist_test'
        )

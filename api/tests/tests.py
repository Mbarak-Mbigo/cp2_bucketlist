import unittest
from flask import current_app

from api import create_app, db


class MainApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

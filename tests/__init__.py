import unittest
import os
import json
from flask_testing import TestCase
from app.models import Bucketlist, Item
from app import create_app, db

class TestBase(TestCase):
    """ Base config for running the tests """
    def setUp(self):

        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Lets go to Lagos'}
        self.items = {'name': 'item1', 'done':'False'}
        self.items_update = {'name': 'item2', 'done':'False'}    

        with self.app.app_context():
            db.create_all()

    def create_app(self):
        return

    def tearDown(self):
        """teardown all initialized variables."""

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
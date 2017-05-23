import unittest
import os
import json
from app.models import Bucketlist, Item
from app import create_app, db


class BaseTestCase(unittest.TestCase):
    """ Base config for running the tests """

    def create_app(self):
        return

    def setUp(self):

        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Lets go to Lagos'}
        self.items = {'name': 'item1', 'done': 'False'}
        self.items_update = {'name': 'item2', 'done': 'False'}

        with self.app.app_context():
            db.create_all()

        self.body = {
            "username": "jimmykimani",
            "password": "python"
        }

        # user login credentials

        url = '/api/v1.0/auth/login/'
        self.response = self.client.post(url, data=json.dumps(
            self.body), content_type="appliaction/json")

        self.data = json.loads(
            self.response.data.decode('utf-8'))

        # A Token is needed to restrict access to certain resources
        # If not included it will result in a 401: Unauthorized Access error.

        self.token = self.data['token']
        # Helps json to accept a JSON encoded entity from the request body.
        # Token prefix comes before the token
        self.headers = {'Authorization': 'Token ' + self.token,
                        'Content_type': 'application/json',
                        'Accept': 'application/json'}

    def tearDown(self):
        """teardown all initialized variables."""

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()

import unittest
import os
import json
from tests import BaseTestCase, register_user

url = '/api/v1/auth/'
data = {
    "username":"jimmykimani",
    "password":"pass1234"
}

class UserTestCase(BaseTestCase):
    """ Test endpoints for users """

    def test_registration(self):
        """ Test for user registration """
        response = self.client.pots(url + 'register', data=data)
        data = json.loads(response.data)
        self.assertTrue(data['message'] == 'Successfully registered.')


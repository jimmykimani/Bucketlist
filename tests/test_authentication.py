import unittest
import os
import json
from tests import BaseTestCase, register_user


class UserTestCase(BaseTestCase):
    """ Test endpoints for users """

    def test_registration(self):
        """ Test for user registration """
        response = register_user(self, 'jimmy', 'pass123')
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Successfully registered.')

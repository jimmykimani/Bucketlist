import unittest
import os
import json
from tests import BaseTestCase
from app import create_app, db


class UserTestCase(BaseTestCase):
    """ Test endpoints for users """

    def test_registration(self):
        """ Test for user registration """
        
        response = self.client.post()(
            '/auth/register',
            data=json.dumps(dict(
                username='jimmy',
                password='andela'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201) 
import unittest
import os
import json
from tests.base import BaseTestCase
from app.models import User


class UserTestCase(BaseTestCase):
    """ Test endpoints for users """

    # ======================================================
    # Tests User Login and Register Resource functionality.
    # ---------------------------------------------------------

    def test_registration(self):
        """ Test for user registration """
        response = self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(dict(
                username='joe',
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered username"""
        self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(dict(
                username='joe',
                password='123456'
            )),
            content_type='application/json'
        )
        response = self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(dict(
                username='joe',
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'User already exists. Please Log in.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 202)

    def test_user_login(self):
        """ Test user login """
        self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(dict(
                username='joe',
                password='123456'
            )),
            content_type='application/json'
        )  
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(dict(
                username='joe',
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == "Whoot! Whoot! You're in")
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_login_with_invalid_password(self):
        """ Test user login """
        self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(dict(
                username='joe',
                password='123456'
            )),
            content_type='application/json'
        )  
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(dict(
                username='joe',
                password='1234567890'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == "Invalid user or Password mismatch.")
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 404)


    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(dict(
                username='jimmy',
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 404)

    # ======================================================
    # EOF
    # ------------------------------------------------------
import unittest
import json
import os

from bucketlist import create_app, db

class BucketlistTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name = 'TESTING')
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Lets go to Lagos'}
        self.user = {'username':'jimmy', 'password':'pass'}
        
        with self.app.app_context():
            db_create_all
        
    def test_create_a_bucketlist(self):
        r = self.client().post('/v1/bucketlist/', data = self.bucketlist)
        self.assertEqual(r.status_code, 201)

    def test_get_all_bucketlists(self):
        r = self.client().post('/v1/bucketlists/', data = self.bucketlist)
        self.assertEqual(r.status_code, 201)
        r = self.client().get('/v1/bucketlists/')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Lets go to Lagos', str(r.data))

    def test_get_bucketlist_by_id(self):
        r = self.client().post('/v1/bucketlist/1/', data = self.bucketlist)
        self.assertEqual(r.status_code, 201)
        r =self.client().get('/v1/bucketlists/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.data), ['id'], 1)

    def test_get_bucketlist_with_invalid_id(self):
        r =self.client().get('/v1/bucketlists/1')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(str(r.data), ['error'])

    def test_update_bucketlist(self):
        r = self.client().post('/v1/bucketlist/', data = self.bucketlist)
        
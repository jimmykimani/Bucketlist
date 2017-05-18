import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name = 'TESTING')
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Lets go to Lagos'}
        self.items= {'name': 'False'}       
        with self.app.app_context():
            db.create_all()


    def test_create_a_bucketlist_item(self):
        """ Tests endpoint can create new item."""
        self.client().post('/api//v1/bucketlist/', data=json.dumps(self.bucketlist))
        r = self.client().post('/api/v1/bucketlist/1/items',
                                data=json.dumps(self.items))
        self.assertEqual(r.status_code, 201)
    
    def test_add_item_with_invalid_bucketlist_id(self):
        """ Test endpint rejects invalid bucketlist id """
        testself.client().post('/api//v1/bucketlist/',
                                data=json.dumps(self.bucketlist))
        r = self.client().post('/api/v1/bucketlist/2/items',
                                data=json.dumps(self.items))
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), ['error'], 'Not Found')

    def test_update_items(self):
        """ Test endpoint updated items succesfully"""

        

import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    def setUp(self):
        
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Lets go to Lagos'}
        self.items = {'name': 'item1', 'done':'False'}
        self.items_update = {'name': 'item2', 'done':'False'}


        with self.app.app_context():
            db.create_all()


    def test_create_a_bucketlist_item(self):
        """ Tests endpoint can create new item."""
        self.client().post('/api//v1/bucketlist/',
                           data=json.dumps(self.bucketlist))
        r = self.client().post('/api/v1/bucketlist/1/items',
                               data=json.dumps(self.items))
        self.assertEqual(r.status_code, 201)

    def test_add_item_with_invalid_bucketlist_id(self):
        """ Test endpint rejects invalid bucketlist id """
        self.client().post('/api//v1/bucketlist/',
                           data=json.dumps(self.bucketlist))
        r = self.client().post('/api/v1/bucketlist/2/items',
                               data=json.dumps(self.items))
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), ['error'],
                         'Not Found')
    def test_get_all_items(self):
        """ Test endpoint gets items succesfully"""
        #create new item
        self.client().post('/api//v1/bucketlist/',
                           data=json.dumps(self.bucketlist))
        r = self.client().post('/api/v1/bucketlist/1/items',
                               data=json.dumps(self.items))
        self.assertEqual(r.status_code, 201)
        #get all items
        r = self.client().get('/api/v1/bucketlist/1/items',
                              data=json.dumps(self.items))
        self.assertEqual(r.status_code, 200)

    def test_get_all_items_by_id(self):
        """ Test endpoint get items by id succesfully"""
        #create new item
        self.client().post('/api//v1/bucketlist/',
                           data=json.dumps(self.bucketlist))
        r = self.client().post('/api/v1/bucketlist/1/items',
                               data=json.dumps(self.items))
        self.assertEqual(r.status_code, 201)
        #get items by id
        r = self.client().get('/api/v1/bucketlist/1/items/1',
                              data=json.dumps(self.items))
        self.assertEqual(r.status_code, 200)

    def test_get_all_items_with_invalid_id(self):
        """ Test endpoint rejects to fetch items with invalid id"""
        #create new item
        self.client().post('/api//v1/bucketlist/',
                           data=json.dumps(self.bucketlist))
        r = self.client().post('/api/v1/bucketlist/1/items',
                               data=json.dumps(self.items))
        self.assertEqual(r.status_code, 201)
        #get items by id
        r = self.client().get('/api/v1/bucketlist/1/items/404',
                              data=json.dumps(self.items))
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), ['error'],
                         'Item not found!')

    def test_update_items(self):
        """ Test endpoint updated items succesfully"""
        #create new item
        self.client().post('/api//v1/bucketlist/',
                           data=json.dumps(self.bucketlist))
        r = self.client().post('/api/v1/bucketlist/1/items',
                               data=json.dumps(self.items))
        self.assertEqual(r.status_code, 201)
        #upadate new item
        r = self.client().post('/api/v1/bucketlist/1/items/1',
                               data=json.dumps(self.items_update))
        self.assertEqual(r.status_code, 200)

    def test_update_non_existant_items(self):
        """ Test that endpoint rejects update with invalid id """
        #create new item
        self.client().post('/api//v1/bucketlist/',
                           data=json.dumps(self.bucketlist))
        r = self.client().post('/api/v1/bucketlist/1/items',
                               data=json.dumps(self.items))
        self.assertEqual(r.status_code, 201)
        #upadate new item
        r = self.client().put('/api/v1/bucketlist/1/items/111',
                              data=json.dumps(self.items_update))
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), ['error'],
                         'Item not found!')        
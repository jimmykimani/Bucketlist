import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name = 'testing')
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Lets go to Lagos'}
        self.user = {'username':'jimmy', 'password':'pass'}

        with self.app.app_context():
            db.create_all()


    def test_create_a_bucketlist(self):
        """ Tests API can create new bucketlist."""
        r = self.client().post('/api//v1/bucketlist/',
                               data=json.dumps(self.bucketlist))
        self.assertEqual(r.status_code, 201)

    def test_get_all_bucketlists(self):
        """ Test API can get all buecketlists """
        r = self.client().post('/api//v1/bucketlists/',
                               data=json.dumps(self.bucketlist))
        self.assertEqual(r.status_code, 201)
        r = self.client().get('/api/v1/bucketlists/')
        self.assertEqual(r.status_code, 200)

    def test_get_bucketlist_by_id(self):
        """ Test API can get bucketlist by id. """
        r = self.client().post('/api//v1/bucketlist/',
                               data=json.dumps(self.bucketlist))
        self.assertEqual(r.status_code, 201)
        r = self.client().get('/v1/bucketlists/1')
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.data)
        self.assertEqual(data['name'], 'Lets go to Lagos')

    def test_get_bucketlist_using_invalid_id(self):
        """ Test API can get bucketlist with invalid id. """
        r = self.client().get('/api//v1/bucketlists/1')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), ['error'], 'Not Found')

    def test_update_bucketlist(self):
        """ Test API can update an existing bucketlist. """
        r = self.client().post('/api//v1/bucketlist/',
                               data=json.dumps(self.bucketlist))
        self.assertEqual(r.status_code, 201)
        #update bucketlist
        new_bucketlist = {'name': 'Lets go to Lagos this weekend!'}
        r = self.client().put('/api/v1/bucketlists/1', data=new_bucketlist)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), ['name'],
                         'Lets go to Lagos this weekend!')

    def test_update_an_inexistent_bucketlist(self):
        """ Test API can update an inexisting bucketlist. """
        r = self.client().put('/api//v1/bucketlists/1',
                              data={'name':'Lets go to Lagos this weekend!'})
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), ['error'], 'Not Found')

    def test_delete_bucketlist(self):
        """Test API can delete an existing bucketlist."""
        r = self.client().post('/api//v1/bucketlist/',
                               data=json.dumps(self.bucketlist))
        self.assertEqual(r.status_code, 201)
        r = self.client().delete('/api/v1/bucketlists/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), ['msg'],
                         'Bucketlist deleted succesfully')

    def test_deleting_non_existing_bucketlist(self):
        """ Test API can delete a non existing bucketlist."""
        r = self.client().post('/api//v1/bucketlist/',
                               data=self.bucketlist)
        self.assertEqual(r.status_code, 201)        
        r = self.client().delete('/api/v1/bucketlists/9')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), ['error'], 'Not Found')
    

    def tearDown(self):
        """teardown all initialized variables."""

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
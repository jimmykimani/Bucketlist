import unittest
import json
import os

from .import create_app, db

class BucketlistTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name = 'TESTING')
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Lets go to Lagos'}
        self.user = {'username':'jimmy', 'password':'pass'}
        
        with self.app.app_context():
            db_create_all()


    def test_create_a_bucketlist(self):
        r = self.client().post('/v1/bucketlist/', data=self.bucketlist)
        self.assertEqual(r.status_code, 201)

    def test_get_all_bucketlists(self):
        r = self.client().post('/v1/bucketlists/', data=self.bucketlist)
        self.assertEqual(r.status_code, 201)
        r = self.client().get('/v1/bucketlists/')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Lets go to Lagos', str(r.data))

    def test_get_bucketlist_by_id(self):
        r = self.client().post('/v1/bucketlist/1/', data=self.bucketlist)
        self.assertEqual(r.status_code, 201)
        r = self.client().get('/v1/bucketlists/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.data), ['id'], 1)

    def test_get_bucketlist_with_invalid_id(self):
        r =self.client().get('/v1/bucketlists/1')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(str(r.data), ['error'])

    def test_update_bucketlist(self):
        """ Test API can update an existing bucketlist. """
        r = self.client().post('/v1/bucketlist/', data=self.bucketlist)
        self.assertEqual(r.status_code, 201)
        r =self.client().put('/v1/bucketlists/1',
                data = {'name': 'Lets go to Lagos this weekend!'})
        self.assertEqual(r.status_code, 200)

    def test_update_an_inexistent_bucketlist(self):
        """ Test API can update an inexisting bucketlist. """
        r =self.client().put('/v1/bucketlists/1',
                data = {'name': 'Lets go to Lagos this weekend!'})
        self.assertEqual(r.status_code, 404)
        self.assertEqual(str(r.data), ['error'])

    def test_delete_bucketlist(self):
        """Test API can delete an existing bucketlist."""
        r = self.client().post('/v1/bucketlist/', data=self.bucketlist)
        self.assertEqual(r.status_code, 201)
        r = self.client().delete('/v1/bucketlists/1')
        self.assertEqual(r.status_code, 200)

    def test_deleting_non_existing_bucketlist(self):
        """ Test API can delete a non existing bucketlist. """
        r = self.client().post('/v1/bucketlist/', data=self.bucketlist)
        self.assertEqual(r.status_code, 201)        
        r = self.client().delete('/v1/bucketlists/9')
        self.assertEqual(r.status_code, 404)        

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()

import os

import json
from tests.base import BaseTestCase
from app.models import Bucketlist, Item


url = '/api/v1/bucketlists/'


class BucketlistTestCase(BaseTestCase):
    """ Test api can create bucketlists. """

    def test_create_a_bucketlist(self):
        """ Tests API can create new bucketlist."""
        bucketlist = {'name': 'Lets go to Lagos'}
        response = self.client.post('/api/v1/bucketlists/',
                                    headers=self.set_header(),
                                    data=json.dumps(bucketlist))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

    def test_create_an_existing_bucketlist(self):
        """ Tests API can't create an existing bucketlist."""
        bucketlist = {'name': 'Lets go to Lagos'}
        self.client.post('/api/v1/bucketlists/',
                         headers=self.set_header(),
                         data=json.dumps(bucketlist))
        response = self.client.post('/api/v1/bucketlists/',
                                    headers=self.set_header(),
                                    data=json.dumps(bucketlist))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 409)

    def test_get_all_bucketlists(self):
        """ Test API can get all buecketlists """
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        response = self.client.get(url, headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_get_bucketlist_by_id(self):
        """ Test API can get bucketlist by id. """
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        response = self.client.get(url + '1/', headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'new bucketlist')

    def test_get_bucketlist_using_invalid_id(self):
        """ Test API can get bucketlist with invalid id. """
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        response = self.client.get(url + '2/', headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)

    def test_update_bucketlist(self):
        """ Test API can update an existing bucketlist. """
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        # update bucketlist
        response = self.client.put(url + '1/',
                                   data=json.dumps(
                                       dict(name='update new bucketlist')),
                                   headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_delete_bucketlist(self):
        """Test API can delete an existing bucketlist."""
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        # delete bucketlist
        response = self.client.delete(url + '1/',
                                      headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['message'] ==
                        'bucketlist with id 1 has been deleted')

    def test_deleting_non_existing_bucketlist(self):
        """ Test API can delete a non existing bucketlist."""
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        # delete bucketlist
        response = self.client.delete(url + '10/',
                                      headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)


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
        response = self.client.get(url +'1/', headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'new bucketlist')

    # def test_get_bucketlist_using_invalid_id(self):
    #     """ Test API can get bucketlist with invalid id. """
    #     r = self.client.get('/api/v1/bucketlists/1')
    #     self.assertEqual(r.status_code, 400)
    #     self.assertEqual(json.loads(r.data), ['error'], 'Not Found')

    # def test_update_bucketlist(self):
    #     """ Test API can update an existing bucketlist. """
    #     r = self.client.post('/api/v1/bucketlist/',
    #                            data=json.dumps(bucketlist), headers=self.headers)
    #     self.assertEqual(r.status_code, 201)
    #     # update bucketlist
    #     new_bucketlist = {'name': 'Lets go to Lagos this weekend!'}
    #     r = self.client.put('/api/v1/bucketlists/1', data=new_bucketlist)
    #     self.assertEqual(r.status_code, 200)
    #     self.assertEqual(json.loads(r.data), ['name'],
    #                      'Lets go to Lagos this weekend!')

    # # def test_update_an_existing_bucketlist(self):
    # #     """ Test API can update an existing bucketlist. """
    # #     r = self.client.put('/api/v1/bucketlists/1',
    # #                           data=json.dumps(bucketlist), headers=self.headers)
    # #     self.assertEqual(r.status_code, 404)
    # #     self.assertEqual(json.loads(r.data), ['error'], 'Not Found')

    # def test_delete_bucketlist(self):
    #     """Test API can delete an existing bucketlist."""
    #     r = self.client.post('/api/v1/bucketlists/',
    #                            data=json.dumps(bucketlist), headers=self.headers)
    #     self.assertEqual(r.status_code, 201)
    #     r = self.client.delete('/api/v1/bucketlists/1/')
    #     self.assertEqual(r.status_code, 200)
    #     self.assertEqual(json.loads(r.data), ['message'],
    #                      'bucketlist with id 1 has been deleted')

    # def test_deleting_non_existing_bucketlist(self):
    #     """ Test API can delete a non existing bucketlist."""
    #     r = self.client.post('/api/v1/bucketlist/',
    #                            data=bucketlist)
    #     self.assertEqual(r.status_code, 201)
    #     r = self.client.delete('/api/v1/bucketlists/9')
    #     self.assertEqual(r.status_code, 404)
    #     self.assertEqual(json.loads(r.data), ['error'], 'Not Found')


import os

import json
from tests.base import BaseTestCase
from app.models import Bucketlist, Item


url = '/api/v1/bucketlists/'
item_url = '/api/v1/bucketlists/1/items/'

# ======================================================
# Tests Buckelist Resource functionality.
# --------------------------------------------------------


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

    def test_get_null_bucketlists(self):
        """ Test API can get null buecketlists """
        response = self.client.get(url + '1/', headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)

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

    # ======================================================
    # Tests Buckelist Item Resource functionality.
    # -------------------------------------------------------

    def test_create_a_bucketlist_item(self):
        """ Tests endpoint can create new item."""
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        response = self.client.post(item_url, data=json.dumps(dict(name='new item')),
                                    headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)

    def test_add_item_with_invalid_bucketlist_id(self):
        """ Test item endpoint rejects invalid bucketlist id """
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        response = self.client.post('/api/v1/bucketlists/99/items/',
                                    data=json.dumps(dict(name='new item')),
                                    headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)

    def test_get_all_items(self):
        """ Test item endpoint gets items succesfully"""
        # create new item
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        self.client.post(item_url, data=json.dumps(dict(name='new item')),
                         headers=self.set_header())
        # get all items
        response = self.client.get(item_url, headers=self.set_header())
        self.assertEqual(response.status_code, 200)

    def test_update_items(self):
        """ Test endpoint updated items succesfully"""
        # create new item
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        self.client.post(item_url, data=json.dumps(dict(name='new item')),
                         headers=self.set_header())
        response = self.client.put(item_url + '1',
                                   data=json.dumps(
                                       dict(name='update new item')),
                                   headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        """ Test delete items """
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        self.client.post(item_url, data=json.dumps(dict(name='new item')),
                         headers=self.set_header())
        response = self.client.delete(item_url + '1',
                                      headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_delete_with_invalid_item_id(self):
        """ Test that endpoint rejects deletion with invalid bucketlist_id """
        # create new item
        self.client.post(url,
                         data=json.dumps(dict(name='new bucketlist')),
                         headers=self.set_header())
        self.client.post(item_url, data=json.dumps(dict(name='new item')),
                                    headers=self.set_header())
        response = self.client.delete(item_url+ '999',
                                   headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)

    # ======================================================
    # EOF
    # ------------------------------------------------------

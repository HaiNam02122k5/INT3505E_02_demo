# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestTransactionsController(BaseTestCase):
    """TransactionsController integration test stubs"""

    def test_delete_transaction(self):
        """Test case for delete_transaction

        Hoàn tất giao dịch (trả sách)
        """
        response = self.client.open(
            '/api/members/{member_id}/transactions/{book_id}'.format(member_id=56, book_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_member_transaction(self):
        """Test case for get_member_transaction

        
        """
        response = self.client.open(
            '/api/members/{member_id}/transactions'.format(member_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_transaction(self):
        """Test case for post_transaction

        Tạo giao dịch mượn sách
        """
        response = self.client.open(
            '/api/members/{member_id}/transactions/{book_id}'.format(member_id=56, book_id=56),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

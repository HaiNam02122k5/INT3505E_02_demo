# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.book import Book  # noqa: E501
from swagger_server.test import BaseTestCase


class TestBooksController(BaseTestCase):
    """BooksController integration tests stubs"""

    def test_delete_book_item(self):
        """Test case for delete_book_item

        Xóa sách (Delete)
        """
        response = self.client.open(
            '/api/books/{book_id}'.format(book_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_book_item(self):
        """Test case for get_book_item

        Lấy thông tin sách theo ID (Read One)
        """
        response = self.client.open(
            '/api/books/{book_id}'.format(book_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_book_list(self):
        """Test case for get_book_list

        Lấy tất cả sách (Read All)
        """
        response = self.client.open(
            '/api/books',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_book_list(self):
        """Test case for post_book_list

        Thêm sách mới (Create)
        """
        body = Book()
        response = self.client.open(
            '/api/books',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_book_item(self):
        """Test case for put_book_item

        Cập nhật thông tin sách (Update)
        """
        body = Book()
        response = self.client.open(
            '/api/books/{book_id}'.format(book_id=56),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.login import Login  # noqa: E501
from swagger_server.models.new_token import NewToken  # noqa: E501
from swagger_server.models.token import Token  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUsersController(BaseTestCase):
    """UsersController integration test stubs"""

    def test_post_refresh_token(self):
        """Test case for post_refresh_token

        Làm mới access token
        """
        response = self.client.open(
            '/api/users/refresh',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_user(self):
        """Test case for post_user

        Tạo JWT khi đăng nhập thành công
        """
        body = Login()
        response = self.client.open(
            '/api/users',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

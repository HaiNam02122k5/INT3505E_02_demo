# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.member import Member  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMemberController(BaseTestCase):
    """MemberController integration test stubs"""

    def test_delete_member_item(self):
        """Test case for delete_member_item

        Xóa thành viên (Delete)
        """
        response = self.client.open(
            '/api/members/{member_id}'.format(member_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_member_item(self):
        """Test case for get_member_item

        Lấy thông tin thành viên theo ID (Read One)
        """
        response = self.client.open(
            '/api/members/{member_id}'.format(member_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_member_list(self):
        """Test case for get_member_list

        Lấy tất cả thành viên (Read All)
        """
        response = self.client.open(
            '/api/members',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_member_list(self):
        """Test case for post_member_list

        Thêm thành viên mới (Create)
        """
        body = Member()
        response = self.client.open(
            '/api/members',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_member_item(self):
        """Test case for put_member_item

        Cập nhật thông tin thành viên (Update)
        """
        body = Member()
        response = self.client.open(
            '/api/members/{member_id}'.format(member_id=56),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

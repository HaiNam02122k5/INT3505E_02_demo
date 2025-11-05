import connexion
import six

from swagger_server.models.member import Member  # noqa: E501
from swagger_server import util


def delete_member_item(member_id):  # noqa: E501
    """Xóa thành viên (Delete)

    Xóa thông tin thành viên # noqa: E501

    :param member_id: Định danh thành viên
    :type member_id: int

    :rtype: None
    """
    return 'do some magic!'


def get_member_item(member_id):  # noqa: E501
    """Lấy thông tin thành viên theo ID (Read One)

    Lấy thông tin thành viên theo ID # noqa: E501

    :param member_id: Định danh thành viên
    :type member_id: int

    :rtype: None
    """
    return 'do some magic!'


def get_member_list():  # noqa: E501
    """Lấy tất cả thành viên (Read All)

    Lấy danh sách tất cả thành viên # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def post_member_list(body):  # noqa: E501
    """Thêm thành viên mới (Create)

    Thêm một thành viên mới # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Member.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def put_member_item(body, member_id):  # noqa: E501
    """Cập nhật thông tin thành viên (Update)

    Cập nhật thông tin thành viên # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param member_id: Định danh thành viên
    :type member_id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = Member.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

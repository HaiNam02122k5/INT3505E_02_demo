import connexion
import six

from swagger_server import util


def delete_transaction(member_id, book_id):  # noqa: E501
    """Hoàn tất giao dịch (trả sách)

    Hoàn tất giao dịch (trả sách) # noqa: E501

    :param member_id: ID thành viên
    :type member_id: int
    :param book_id: ID sách
    :type book_id: int

    :rtype: None
    """
    return 'do some magic!'


def get_member_transaction(member_id):  # noqa: E501
    """get_member_transaction

    Lấy tất cả giao dịch của 1 thành viên # noqa: E501

    :param member_id: ID thành viên
    :type member_id: int

    :rtype: None
    """
    return 'do some magic!'


def post_transaction(member_id, book_id):  # noqa: E501
    """Tạo giao dịch mượn sách

    Tạo giao dịch mượn sách # noqa: E501

    :param member_id: ID thành viên
    :type member_id: int
    :param book_id: ID sách
    :type book_id: int

    :rtype: None
    """
    return 'do some magic!'

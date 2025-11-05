import connexion
import six

from swagger_server.models.book import Book  # noqa: E501
from swagger_server import util


def delete_book_item(book_id):  # noqa: E501
    """Xóa sách (Delete)

    Xóa sách # noqa: E501

    :param book_id: Định danh của cuốn sách
    :type book_id: int

    :rtype: None
    """
    return 'do some magic!'


def get_book_item(book_id):  # noqa: E501
    """Lấy thông tin sách theo ID (Read One)

    Lấy thông tin sách theo ID # noqa: E501

    :param book_id: Định danh của cuốn sách
    :type book_id: int

    :rtype: None
    """
    return 'do some magic!'


def get_book_list():  # noqa: E501
    """Lấy tất cả sách (Read All)

    Lấy danh sách tất cả sách # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def post_book_list(body):  # noqa: E501
    """Thêm sách mới (Create)

    Thêm một cuốn sách mới # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def put_book_item(body, book_id):  # noqa: E501
    """Cập nhật thông tin sách (Update)

    Cập nhật thông tin sách # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param book_id: Định danh của cuốn sách
    :type book_id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

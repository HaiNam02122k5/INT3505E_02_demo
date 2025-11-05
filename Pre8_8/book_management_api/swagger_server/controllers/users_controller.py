import connexion
import six

from swagger_server.models.login import Login  # noqa: E501
from swagger_server.models.new_token import NewToken  # noqa: E501
from swagger_server.models.token import Token  # noqa: E501
from swagger_server import util


def post_refresh_token():  # noqa: E501
    """Làm mới access token

    Làm mới Access Token bằng Refresh Token # noqa: E501


    :rtype: NewToken
    """
    return 'do some magic!'


def post_user(body):  # noqa: E501
    """Tạo JWT khi đăng nhập thành công

    Lấy Access Token để sử dụng các API khác # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Token
    """
    if connexion.request.is_json:
        body = Login.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

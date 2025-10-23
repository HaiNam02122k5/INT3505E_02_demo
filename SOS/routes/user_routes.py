from flask_restx import Resource
from SOS.services import UserService

def init_user_routes(api, user_ns, schemas):
    """Khởi tạo route cho User"""

    @user_ns.route('')
    class User(Resource):
        @user_ns.doc(description='Lấy Access Token để sử dụng các API khác')
        @user_ns.expect(schemas['login'], validate=True)
        @user_ns.response(200, 'Đăng nhập thành công', schemas['token'])
        @user_ns.response(401, 'Thông tin đăng nhập không hợp lệ')
        def post(self):
            """Tạo JWT khi đăng nhập thành công"""
            data = self.api.payload
            return UserService.authenticate(data['username'], data['password'])
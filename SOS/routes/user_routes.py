from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from SOS.services import UserService

def init_user_routes(api, user_ns, schemas):
    """Khởi tạo route cho User"""

    @user_ns.route('')
    class UserRegistration(Resource):
        @user_ns.doc(
            description='Tạo tài khoản người dùng mới (Đăng ký)',
            security='jwt'
        )
        @user_ns.expect(schemas['login'], validate=True)
        @user_ns.response(201, 'Tài khoản được tạo thành công')
        @user_ns.response(400, 'Dữ liệu không hợp lệ (ví dụ: username đã tồn tại)')
        @jwt_required()
        def post(self):
            """Tạo một người dùng mới"""
            data = self.api.payload
            return UserService.create_user(data['username'], data['password'])

    @user_ns.route('/login')
    class User(Resource):
        @user_ns.doc(description='Lấy Access Token để sử dụng các API khác')
        @user_ns.expect(schemas['login'], validate=True)
        @user_ns.response(200, 'Đăng nhập thành công', schemas['token'])
        @user_ns.response(401, 'Thông tin đăng nhập không hợp lệ')
        def post(self):
            """Tạo JWT khi đăng nhập thành công"""
            data = self.api.payload
            return UserService.authenticate(data['username'], data['password'])

    @user_ns.route('/refresh')
    class RefreshToken(Resource):
        @user_ns.doc(
            description='Làm mới Access Token bằng Refresh Token',
            security='jwt'
        )
        @user_ns.response(200, 'Token mới được tạo thành công', schemas['new_token'])
        @user_ns.response(401, 'Refresh token không hợp lệ hoặc hết hạn')
        @jwt_required(refresh=True)  # ← YÊU CẦU REFRESH TOKEN
        def post(self):
            """Làm mới access token"""
            current_user_id = get_jwt_identity()
            return UserService.refresh_access_token(current_user_id)
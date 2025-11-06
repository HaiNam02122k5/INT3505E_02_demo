from SOS.models.user import User
from SOS.extensions import db
from flask_jwt_extended import create_access_token, create_refresh_token

class UserService:
    @staticmethod
    def authenticate(username, password):
        """Xác thực người dùng"""
        user = User.query.filter_by(username=username).first()

        if user and password == user.password:
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {"msg": "Tên đăng nhập hoặc mật khẩu không đúng"}, 401

    @staticmethod
    def refresh_access_token(user_id):
        """Tạo access token mới từ refresh token"""
        new_access_token = create_access_token(identity=user_id)
        return {'access_token': new_access_token}, 200

    @staticmethod
    def create_user(username, password):
        """Tạo người dùng mới"""
        if User.query.filter_by(username=username).first():
            return {'message': 'Username đã tồn tại'}, 409

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Tạo user thành công'}, 201

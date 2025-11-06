import pytest
from SOS.services.user_service import UserService
from SOS.models.user import User


@pytest.mark.unit
class TestUserService:
    """Test UserService methods"""

    def test_authenticate_success(self, db_session, test_user):
        """Test xác thực thành công"""
        result, status = UserService.authenticate('testuser', 'testpass123')

        assert status == 200
        assert 'access_token' in result
        assert 'refresh_token' in result

    def test_authenticate_wrong_password(self, db_session, test_user):
        """Test xác thực với mật khẩu sai"""
        result, status = UserService.authenticate('testuser', 'wrongpass')

        assert status == 401
        assert 'msg' in result

    def test_authenticate_user_not_found(self, db_session):
        """Test xác thực với user không tồn tại"""
        result, status = UserService.authenticate('nonexistent', 'password')

        assert status == 401

    def test_create_user_success(self, db_session):
        """Test tạo user mới thành công"""
        result, status = UserService.create_user('newuser', 'newpass123')

        assert status == 201
        assert result['message'] == 'Tạo user thành công'

        # Verify user exists
        user = User.query.filter_by(username='newuser').first()
        assert user is not None

    def test_create_user_duplicate_username(self, db_session, test_user):
        """Test tạo user với username trùng"""
        result, status = UserService.create_user('testuser', 'password')

        assert status == 409
        assert 'đã tồn tại' in result['message']

    def test_refresh_access_token(self, app, test_user):
        """Test làm mới access token"""
        with app.app_context():
            result, status = UserService.refresh_access_token(str(test_user.id))

            assert status == 200
            assert 'access_token' in result
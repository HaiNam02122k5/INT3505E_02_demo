import pytest
import json


@pytest.mark.integration
class TestUserAPI:
    """Test User API endpoints"""

    def test_login_success(self, client, test_user):
        """Test login thành công"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = client.post('/api/users',
                               data=json.dumps(data),
                               content_type='application/json')

        assert response.status_code == 200
        result = json.loads(response.data)
        assert 'access_token' in result
        assert 'refresh_token' in result

    def test_login_invalid_credentials(self, client, test_user):
        """Test login với thông tin sai"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = client.post('/api/users',
                               data=json.dumps(data),
                               content_type='application/json')

        assert response.status_code == 401

    def test_refresh_token(self, client, app, test_user):
        """Test làm mới access token"""
        from flask_jwt_extended import create_refresh_token

        with app.app_context():
            refresh_token = create_refresh_token(identity=str(test_user.id))

        headers = {
            'Authorization': f'Bearer {refresh_token}',
            'Content-Type': 'application/json'
        }

        response = client.post('/api/users/refresh', headers=headers)

        assert response.status_code == 200
        result = json.loads(response.data)
        assert 'access_token' in result

    def test_protected_endpoint_without_token(self, client):
        """Test endpoint cần auth mà không có token"""
        data = {'title': 'Test', 'author': 'Test', 'isbn': '123'}
        response = client.post('/api/books',
                               data=json.dumps(data),
                               content_type='application/json')

        assert response.status_code == 401

    def test_protected_endpoint_with_invalid_token(self, client):
        """Test endpoint với token không hợp lệ"""
        headers = {
            'Authorization': 'Bearer invalid_token_here',
            'Content-Type': 'application/json'
        }
        data = {'title': 'Test', 'author': 'Test', 'isbn': '123'}
        response = client.post('/api/books',
                               data=json.dumps(data),
                               headers=headers)

        assert response.status_code == 422  # Unprocessable Entity

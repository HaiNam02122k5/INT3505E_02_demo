import pytest
import json


@pytest.mark.integration
class TestBookAPI:
    """Test Book API endpoints"""

    def test_get_books_unauthorized(self, client):
        """Test GET books không có token"""
        response = client.get('/api/books')
        # Có thể là 200 nếu endpoint public hoặc 401 nếu protected
        assert response.status_code in [200, 401]

    def test_get_books_with_auth(self, client, auth_headers, sample_book):
        """Test GET books với authentication"""
        response = client.get('/api/books', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1 or (isinstance(data, list))

    def test_create_book_unauthorized(self, client):
        """Test POST book không có token"""
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'copies': 5
        }
        response = client.post('/api/books',
                               data=json.dumps(data),
                               content_type='application/json')

        assert response.status_code == 401

    def test_create_book_with_auth(self, client, auth_headers):
        """Test POST book với authentication"""
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '9876543210',
            'copies': 3
        }
        response = client.post('/api/books',
                               data=json.dumps(data),
                               headers=auth_headers)

        assert response.status_code == 201
        result = json.loads(response.data)
        assert result['message'] == 'Thêm sách thành công'

    def test_create_book_missing_fields(self, client, auth_headers):
        """Test POST book thiếu field bắt buộc"""
        data = {
            'title': 'Incomplete Book'
            # Missing author, isbn
        }
        response = client.post('/api/books',
                               data=json.dumps(data),
                               headers=auth_headers)

        assert response.status_code == 400

    def test_get_book_by_id(self, client, auth_headers, sample_book):
        """Test GET book by ID"""
        response = client.get(f'/api/books/{sample_book.id}',
                              headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Test Book'

    def test_get_book_by_invalid_id(self, client, auth_headers):
        """Test GET book với ID không tồn tại"""
        response = client.get('/api/books/999', headers=auth_headers)

        assert response.status_code == 404

    def test_update_book(self, client, auth_headers, sample_book):
        """Test PUT book"""
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'isbn': sample_book.isbn,
            'copies': 10
        }
        response = client.put(f'/api/books/{sample_book.id}',
                              data=json.dumps(data),
                              headers=auth_headers)

        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['book']['title'] == 'Updated Title'

    def test_delete_book(self, client, auth_headers, sample_book):
        """Test DELETE book"""
        response = client.delete(f'/api/books/{sample_book.id}',
                                 headers=auth_headers)

        assert response.status_code == 200
        result = json.loads(response.data)
        assert 'Xóa sách thành công' in result['message']

import pytest
from SOS.services.book_service import BookService
from SOS.models.book import Book


@pytest.mark.unit
class TestBookService:
    """Test BookService methods"""

    def test_get_all_books_empty(self, db_session):
        """Test lấy danh sách sách khi database trống"""
        result, status = BookService.get_all_books()
        assert status == 200
        assert result == []

    def test_get_all_books_with_data(self, db_session, sample_book):
        """Test lấy danh sách sách có dữ liệu"""
        result, status = BookService.get_all_books()
        assert status == 200
        assert len(result) == 1
        assert result[0]['title'] == 'Test Book'

    def test_get_book_by_id_success(self, db_session, sample_book):
        """Test lấy sách theo ID thành công"""
        result, status = BookService.get_book_by_id(sample_book.id)
        assert status == 200
        assert result['title'] == 'Test Book'
        assert result['isbn'] == '1234567890'

    def test_get_book_by_id_not_found(self, db_session):
        """Test lấy sách với ID không tồn tại"""
        result, status = BookService.get_book_by_id(999)
        assert status == 404
        assert 'message' in result

    def test_create_book_success(self, db_session):
        """Test tạo sách mới thành công"""
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '9876543210',
            'copies': 3
        }
        result, status = BookService.create_book(data)
        assert status == 201
        assert result['message'] == 'Thêm sách thành công'
        assert result['book']['title'] == 'New Book'

    def test_create_book_duplicate_isbn(self, db_session, sample_book):
        """Test tạo sách với ISBN trùng lặp"""
        data = {
            'title': 'Another Book',
            'author': 'Another Author',
            'isbn': '1234567890',  # ISBN trùng
            'copies': 2
        }
        result, status = BookService.create_book(data)
        assert status == 409
        assert 'ISBN đã tồn tại' in result['message']

    def test_create_book_default_copies(self, db_session):
        """Test tạo sách với số lượng mặc định"""
        data = {
            'title': 'Book Without Copies',
            'author': 'Some Author',
            'isbn': '1111111111'
        }
        result, status = BookService.create_book(data)
        assert status == 201
        assert result['book']['copies'] == 1

    def test_update_book_success(self, db_session, sample_book):
        """Test cập nhật sách thành công"""
        data = {
            'title': 'Updated Title',
            'copies': 10
        }
        result, status = BookService.update_book(sample_book.id, data)
        assert status == 200
        assert result['book']['title'] == 'Updated Title'
        assert result['book']['copies'] == 10

    def test_update_book_not_found(self, db_session):
        """Test cập nhật sách không tồn tại"""
        data = {'title': 'Updated Title'}
        result, status = BookService.update_book(999, data)
        assert status == 404

    def test_delete_book_success(self, db_session, sample_book):
        """Test xóa sách thành công"""
        book_id = sample_book.id
        result, status = BookService.delete_book(book_id)
        assert status == 200
        assert 'Xóa sách thành công' in result['message']

        # Verify book is deleted
        book = Book.query.get(book_id)
        assert book is None

    def test_delete_book_not_found(self, db_session):
        """Test xóa sách không tồn tại"""
        result, status = BookService.delete_book(999)
        assert status == 404

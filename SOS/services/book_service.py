from SOS.models.book import Book
from SOS.extensions import db, cache

class BookService:
    @staticmethod
    def get_all_books():
        """Lấy tất cả sách"""
        books = Book.query.all()
        return [book.to_dict() for book in books], 200

    @staticmethod
    def get_book_by_id(book_id):
        """Lấy sách theo ID"""
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Không tìm thấy sách.'}, 404
        return book.to_dict(), 200

    @staticmethod
    def create_book(data):
        """Tạo sách mới"""
        if Book.query.filter_by(isbn=data['isbn']).first():
            return {'message': 'ISBN đã tồn tại.'}, 409

        new_book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            copies=data.get('copies', 1)
        )

        try:
            db.session.add(new_book)
            cache.clear()
            db.session.commit()
            return {'message': 'Thêm sách thành công', 'book': new_book.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi DB: {e}'}, 500

    @staticmethod
    def update_book(book_id, data):
        """Cập nhật sách"""
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Không tìm thấy sách.'}, 404

        try:
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            book.isbn = data.get('isbn', book.isbn)
            book.copies = data.get('copies', book.copies)

            cache.clear()
            db.session.commit()
            return {'message': 'Cập nhật thành công', 'book': book.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi khi cập nhật sách: {e}'}, 500

    @staticmethod
    def delete_book(book_id):
        """Xóa sách"""
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Không tìm thấy sách.'}, 404

        try:
            db.session.delete(book)
            cache.clear()
            db.session.commit()
            return {'message': 'Xóa sách thành công.'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi khi xóa sách: {e}'}, 500

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
# Cấu hình cơ sở dữ liệu SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    """Mô hình cho Sách"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    # 0: available (sẵn có), 1: borrowed (đang mượn)
    status = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self):
        """Chuyển đổi đối tượng Book sang dictionary để trả về JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'status': 'borrowed' if self.status == 1 else 'available'
        }


class Transaction(db.Model):
    """Mô hình cho Giao dịch Mượn/Trả"""
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrower_name = db.Column(db.String(100), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)  # None nếu chưa được trả

    book = db.relationship('Book', backref=db.backref('transactions', lazy=True))

    def to_dict(self):
        """Chuyển đổi đối tượng Transaction sang dictionary để trả về JSON"""
        return {
            'id': self.id,
            'book_id': self.book_id,
            'book_title': self.book.title,
            'borrower_name': self.borrower_name,
            'borrow_date': self.borrow_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'is_open': self.return_date is None
        }


with app.app_context():
    db.create_all()

@app.route('/api/')
def start():
    return "Chào mừng đến với Thư Viện!"

@app.route('/api/books', methods=['POST'])
def create_book():
    """Thêm sách mới (Create)"""
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'author', 'isbn')):
        return jsonify({'message': 'Thiếu trường dữ liệu cần thiết (title, author, isbn)'}), 400

    if Book.query.filter_by(isbn=data['isbn']).first():
        return jsonify({'message': 'ISBN đã tồn tại.'}), 409

    new_book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn']
    )
    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Thêm sách thành công', 'book': new_book.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Lỗi DB: {e}'}), 500


@app.route('/api/books', methods=['GET'])
def get_all_books():
    """Lấy tất cả sách (Read All)"""
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Lấy thông tin sách theo ID (Read One)"""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Không tìm thấy sách.'}), 404
    return jsonify(book.to_dict()), 200


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Cập nhật thông tin sách (Update)"""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Không tìm thấy sách.'}), 404

    data = request.get_json()
    try:
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        # Không cho phép cập nhật trạng thái qua endpoint này, chỉ qua giao dịch

        db.session.commit()
        return jsonify({'message': 'Cập nhật thành công', 'book': book.to_dict()}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Lỗi khi cập nhật sách.'}), 500


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Xóa sách (Delete)"""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Không tìm thấy sách.'}), 404

    if book.status == 1:
        return jsonify({'message': 'Không thể xóa sách đang được mượn.'}), 403

    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Xóa sách thành công.'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Lỗi khi xóa sách.'}), 500


@app.route('/api/borrow', methods=['POST'])
def borrow_book_api():
    """Tạo giao dịch mượn sách"""
    data = request.get_json()
    required_fields = ('book_id', 'borrower_name')
    if not data or not all(k in data for k in required_fields):
        return jsonify({'message': 'Thiếu book_id hoặc borrower_name.'}), 400

    book = Book.query.get(data['book_id'])
    if not book:
        return jsonify({'message': 'Không tìm thấy sách với ID này.'}), 404

    if book.status == 1:
        return jsonify({'message': 'Sách hiện đang được mượn.'}), 409  # Conflict

    # Tạo giao dịch mới
    new_transaction = Transaction(
        book_id=book.id,
        borrower_name=data['borrower_name']
    )

    try:
        db.session.add(new_transaction)
        # Cập nhật trạng thái sách
        book.status = 1
        db.session.commit()
        return jsonify({'message': 'Mượn sách thành công', 'transaction': new_transaction.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Lỗi khi mượn sách: {e}'}), 500


@app.route('/api/return/<int:book_id>', methods=['POST'])
def return_book_api(book_id):
    """Hoàn tất giao dịch (trả sách)"""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Không tìm thấy sách với ID này.'}), 404

    if book.status == 0:
        return jsonify({'message': 'Sách hiện đã sẵn có (chưa được mượn).'}), 409  # Conflict

    # Tìm giao dịch MỞ (chưa có ngày trả) cho cuốn sách này
    transaction = Transaction.query.filter_by(book_id=book_id, return_date=None).first()

    if not transaction:
        # Trường hợp hiếm khi DB bị lỗi trạng thái
        return jsonify({'message': 'Không tìm thấy giao dịch mở cho sách này.'}), 404

    try:
        # 1. Cập nhật ngày trả
        transaction.return_date = datetime.utcnow()
        # 2. Cập nhật trạng thái sách
        book.status = 0

        db.session.commit()
        return jsonify({'message': 'Trả sách thành công', 'transaction': transaction.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Lỗi khi trả sách: {e}'}), 500


@app.route('/api/transactions/open', methods=['GET'])
def get_open_transactions():
    """Lấy danh sách các giao dịch đang mở (sách đang mượn)"""
    open_transactions = Transaction.query.filter(Transaction.return_date == None).all()
    return jsonify([t.to_dict() for t in open_transactions]), 200


if __name__ == '__main__':
    app.run(debug=True)
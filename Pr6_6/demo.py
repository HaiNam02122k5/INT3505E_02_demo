from flask import Flask, jsonify, request, abort
from models import db, Book, User, Author, Transaction

app = Flask(__name__)

# --- Cấu hình database ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# --- CƠ SỞ DỮ LIỆU GIẢ LẬP TẠI CHỖ (IN-MEMORY DATABASE) ---
# Sử dụng dictionary để lưu trữ dữ liệu
users = {
    1: {"id": 1, "name": "Alice Smith", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob Johnson", "email": "bob@example.com"},
}
authors = {
    1: {"id": 1, "name": "Jane Austen"},
    2: {"id": 2, "name": "George Orwell"},
}
books = {
    101: {"id": 101, "title": "Pride and Prejudice", "author_id": 1, "isbn": "978-0141439518"},
    102: {"id": 102, "title": "1984", "author_id": 2, "isbn": "978-0451524935"},
    103: {"id": 103, "title": "Emma", "author_id": 1, "isbn": "978-0141439587"},
}
borrow_records = [
    {"record_id": 1, "user_id": 1, "book_id": 101, "borrow_date": "2023-10-01", "return_date": None},
    {"record_id": 2, "user_id": 2, "book_id": 102, "borrow_date": "2023-09-15", "return_date": "2023-10-10"},
]
next_user_id = 3
next_book_id = 104
next_record_id = 3


# --- API CHO NGƯỜI DÙNG (USERS) ---
@app.route('/users', methods=['GET'])
def get_users():
    """Lấy danh sách tất cả người dùng."""
    # Trả về danh sách các giá trị (người dùng) từ dictionary users
    return jsonify(list(users.values()))


@app.route('/users', methods=['POST'])
def create_user():
    """Tạo người dùng mới."""
    global next_user_id
    if not request.json or 'name' not in request.json or 'email' not in request.json:
        abort(400, description="Dữ liệu thiếu 'name' hoặc 'email'")

    new_user = {
        'id': next_user_id,
        'name': request.json['name'],
        'email': request.json['email']
    }
    users[next_user_id] = new_user
    next_user_id += 1
    return jsonify(new_user), 201  # 201 Created


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Lấy thông tin một người dùng cụ thể."""
    user = users.get(user_id)
    if user is None:
        abort(404, description=f"Không tìm thấy người dùng với ID: {user_id}")
    return jsonify(user)


@app.route('/users/<int:user_id>/borrow_records', methods=['GET'])
def get_user_borrow_records(user_id):
    """Lấy danh sách các lần mượn sách của một người dùng."""
    if user_id not in users:
        abort(404, description=f"Không tìm thấy người dùng với ID: {user_id}")

    records = [record for record in borrow_records if record['user_id'] == user_id]
    return jsonify(records)


# --- API CHO TÁC GIẢ (AUTHORS) ---

@app.route('/authors', methods=['GET'])
def get_authors():
    """Lấy danh sách tất cả tác giả."""
    return jsonify(list(authors.values()))


# --- API CHO SÁCH (BOOKS) ---

@app.route('/books', methods=['GET'])
def get_books():
    """Lấy danh sách tất cả sách."""
    return jsonify(list(books.values()))


@app.route('/books/<int:book_id>/borrow_records', methods=['GET'])
def get_book_borrow_records(book_id):
    """Lấy danh sách các lần mượn sách của một cuốn sách."""
    if book_id not in books:
        abort(404, description=f"Không tìm thấy sách với ID: {book_id}")

    records = [record for record in borrow_records if record['book_id'] == book_id]
    return jsonify(records)


if __name__ == '__main__':
    # Chạy ứng dụng Flask ở chế độ Debug (gỡ lỗi)
    app.run(debug=True)
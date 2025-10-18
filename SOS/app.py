from datetime import datetime, timedelta

from flask import Flask
from flask_caching import Cache
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Cấu hình cơ sở dữ liệu SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cấu hình JWT
app.config["JWT_SECRET_KEY"] = "SOS"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

# Cấu hình Cache
app.config['CACHE_TYPE'] = 'SimpleCache'
    # Thời gian timeout tính theo giây
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# Cấu hình Swagger tự động
authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input field: **Bearer <JWT>**, where JWT is the access token"
    }
}

api = Api(
    app,
    version="1.0",
    title="Book Management API",
    description="Tài liệu API tự động sinh bằng Flask-RESTX",
    doc="/docs/",
    security='jwt', # Mặc định bảo vệ tất cả endpoint
    authorizations=authorizations # Định nghĩa cách thức bảo vệ
)

user_ns = api.namespace("Users", path="/api/users", description="CRUD operations for users")
book_ns = api.namespace("Books", path="/api/books", description="CRUD operations for books")
transaction_ns = api.namespace("Transactions", path="/api/transactions", description="CRUD operations for transactions")

# --- Mô hình dữ liệu Swagger ---
login_model = api.model('Login', {
    'username': fields.String(required=True, description='Tên đăng nhập'),
    'password': fields.String(required=True, description='Mật khẩu')
})

book_model = api.model('Book', {
    'id': fields.Integer(readonly=True, description='Book ID'),
    'title': fields.String(required=True, description='Book title'),
    'author': fields.String(required=True, description='Book author'),
    'isbn': fields.String(description='Book ISBN'),
    'copies': fields.Integer(description='Book copies')
})

transaction_model = api.model('Transaction', {
    'id': fields.Integer(readonly=True, description='Transaction ID'),
    'book_id': fields.Integer(readonly=True, description='Book ID'),
    'borrower_id': fields.Integer(readonly=True, description='Borrower ID'),
    'borrow_date': fields.String(readonly=True, description='Borrow Date'),
'   return_date': fields.String(readonly=True, description='Return Date')
})

db = SQLAlchemy(app)
jwt = JWTManager(app)
cache = Cache(app)

class User(db.Model):
    """Mô hình người dùng đơn giản cho mục đích minh họa"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Book(db.Model):
    """Mô hình cho Sách"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    copies = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Chuyển đổi đối tượng Book sang dictionary để trả về JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'copies': self.copies
        }

class Transaction(db.Model):
    """Mô hình cho Giao dịch Mượn/Trả"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)  # None nếu chưa được trả

    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
    book = db.relationship('Book', backref=db.backref('transactions', lazy=True))

    def to_dict(self):
        """Chuyển đổi đối tượng Transaction sang dictionary để trả về JSON"""
        return {
            'id': self.id,
            'book_id': self.book_id,
            'book_title': self.book.title,
            'borrower_id': self.user_id,
            'borrower_name': self.user.username,
            'borrow_date': self.borrow_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None
        }

with app.app_context():
    db.create_all()
    if not User.query.first():
        admin_user = User(username='admin', password='12345678') # Mật khẩu Pr5_5
        db.session.add(admin_user)
        db.session.commit()

@app.route('/api/')
def start():
    return "Chào mừng đến với Thư Viện!"

"""------------USER---------------"""
@user_ns.route('/login')
class Login(Resource):
    @user_ns.doc(description='Lấy Access Token để sử dụng các API khác')
    @user_ns.expect(login_model, validate=True)
    @user_ns.response(200, 'Đăng nhập thành công', api.model('Token', {'access_token': fields.String()}))
    @user_ns.response(401, 'Thông tin đăng nhập không hợp lệ')
    def post(self):
        """Tạo JWT khi đăng nhập thành công"""
        data = self.api.payload
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and password == user.password:
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}, 200
        else:
            return {"msg": "Tên đăng nhập hoặc mật khẩu không đúng"}, 401

"""------------BOOK---------------"""
@book_ns.route('')
class BookList(Resource):
    @book_ns.doc(
        security='jwt',
        description='Lấy danh sách tất cả sách',
        responses={200: 'Thành công'}
    )
    @cache.cached(timeout=60)
    def get(self):
        """Lấy tất cả sách (Read All)"""
        books = Book.query.all()
        return [book.to_dict() for book in books], 200

    @book_ns.doc(
        security='jwt',
        description='Thêm một cuốn sách mới',
        responses={
            201: 'Sách được tạo thành công',
            400: 'Thiếu dữ liệu',
            401: 'Chưa được xác thực',
            409: 'ISBN đã tồn tại'
        }
    )
    @book_ns.expect(book_model, validate=True) # Yêu cầu đầu vào phải theo book_model
    @jwt_required()
    def post(self):
        """Thêm sách mới (Create)"""
        current_user_id = get_jwt_identity()
        data = self.api.payload # Lấy dữ liệu từ payload (body)

        if Book.query.filter_by(isbn=data['isbn']).first():
            return {'message': 'ISBN đã tồn tại.'}, 409

        new_book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            copies=data.get('copies', 1) # Mặc định là 1 bản sao
        )
        try:
            db.session.add(new_book)
            cache.clear()
            db.session.commit()
            return {'message': 'Thêm sách thành công', 'book': new_book.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi DB: {e}'}, 500

@book_ns.route('/<int:book_id>')
@book_ns.param('book_id', 'Định danh của cuốn sách')
class BookItem(Resource):
    @book_ns.doc(description='Lấy thông tin sách theo ID')
    @cache.cached(timeout=120)
    def get(self, book_id):
        """Lấy thông tin sách theo ID (Read One)"""
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Không tìm thấy sách.'}, 404
        return book.to_dict(), 200

    @book_ns.doc(description='Cập nhật thông tin sách')
    @book_ns.expect(book_model)
    @jwt_required()
    def put(self, book_id):
        """Cập nhật thông tin sách (Update)"""
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Không tìm thấy sách.'}, 404

        data = self.api.payload
        try:
            # Chỉ cập nhật các trường được cung cấp trong payload
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

    @book_ns.doc(description='Xóa sách')
    @jwt_required()
    def delete(self, book_id):
        """Xóa sách (Delete)"""
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Không tìm thấy sách.'}, 404

        if book.copies != Book.query.get(book_id).copies:
             return {'message': 'Không thể xóa sách đang có giao dịch mượn.'}, 403

        try:
            db.session.delete(book)
            cache.clear()
            db.session.commit()
            return {'message': 'Xóa sách thành công.'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi khi xóa sách: {e}'}, 500

"""------------TRANSACTION---------------"""


@transaction_ns.route('/borrow')  # Dùng chung namespace với sách
class BorrowBook(Resource):
    @book_ns.doc(description='Tạo giao dịch mượn sách')
    @book_ns.expect(transaction_model, validate=True)
    @jwt_required()
    def post(self):
        """Tạo giao dịch mượn sách"""
        data = self.api.payload
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return {'message': 'Không tìm thấy người mượn với ID này.'}, 404

        book = Book.query.get(data['book_id'])
        if not book:
            return {'message': 'Không tìm thấy sách với ID này.'}, 404

        # Nếu không còn bản sao nào
        if book.copies <= 0:
            return {'message': 'Sách hiện đã được mượn hết.'}, 409

        # Tạo giao dịch mới
        new_transaction = Transaction(
            book_id=book.id,
            user_id=int(current_user_id)
        )

        try:
            db.session.add(new_transaction)
            book.copies = book.copies - 1
            cache.clear()
            db.session.commit()
            return {'message': 'Mượn sách thành công', 'transaction': new_transaction.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi khi mượn sách: {e}'}, 500

@transaction_ns.route('/return/<int:book_id>')
@transaction_ns.param('book_id', 'ID của cuốn sách được trả')
class ReturnBook(Resource):
    @book_ns.doc(description='Hoàn tất giao dịch (trả sách)')
    @jwt_required()
    def post(self, book_id):
        """Hoàn tất giao dịch (trả sách)"""
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id)) # Vì identity được lưu dưới dạng str

        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Không tìm thấy sách với ID này.'}, 404

        # Tìm giao dịch MỞ cho cuốn sách này và người dùng này
        transaction = Transaction.query.filter_by(
            book_id=book_id,
            user_id=int(current_user_id),  # <--- Dùng user_id để lọc
            return_date=None
        ).first()

        if not transaction:
            return {'message': 'Không tìm thấy giao dịch mở cho sách này của bạn.'}, 404

        try:
            transaction.return_date = datetime.utcnow()
            book.copies = book.copies + 1

            cache.clear()
            db.session.commit()
            return {'message': 'Trả sách thành công', 'transaction': transaction.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi khi trả sách: {e}'}, 500


if __name__ == '__main__':
    app.run(debug=True)
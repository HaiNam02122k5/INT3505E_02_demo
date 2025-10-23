from datetime import timedelta

from flask import Flask
from flask_jwt_extended import jwt_required
from flask_restx import Api, Resource, fields

from SOS.extensions import jwt, db, cache
from SOS.models import User
from SOS.services import BookService, UserService, TransactionService, MemberService

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
transaction_ns = api.namespace("Transactions", path="/api/<int:member_id>/transactions", description="CRUD operations for transactions")
member_ns = api.namespace("Member", path="/api/members", description="CRUD operations for members")

# --- Mô hình dữ liệu Swagger ---
login_model = api.model('Login', {
    'username': fields.String(required=True, description='Tên đăng nhập'),
    'password': fields.String(required=True, description='Mật khẩu')
})

book_model = api.model('Book', {
    'id': fields.Integer(readonly=True, description='Book ID'),
    'title': fields.String(required=True, description='Tiêu đề'),
    'author': fields.String(required=True, description='Tác giả'),
    'isbn': fields.String(description='Book ISBN'),
    'copies': fields.Integer(description='Số lượng')
})

member_model = api.model('Member', {
    'id': fields.Integer(readonly=True, description='Member ID'),
    'name': fields.String(required=True, description='Họ và tên'),
    'phone_number': fields.String(required=True, description='Số điện thoại'),
    'address': fields.String(required=True, description='Địa chỉ')
})

db.init_app(app)
jwt.init_app(app)
cache.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.first():
        admin_user = User(username='admin', password='12345678')
        db.session.add(admin_user)
        db.session.commit()

@app.route('/api/')
def start():
    return "Chào mừng đến với Thư Viện!"

"""------------USER---------------"""
@user_ns.route('')
class User(Resource):
    @user_ns.doc(description='Lấy Access Token để sử dụng các API khác')
    @user_ns.expect(login_model, validate=True)
    @user_ns.response(200, 'Đăng nhập thành công', api.model('Token', {'access_token': fields.String()}))
    @user_ns.response(401, 'Thông tin đăng nhập không hợp lệ')
    def post(self):
        """Tạo JWT khi đăng nhập thành công"""
        data = self.api.payload
        return UserService.authenticate(data['username'], data['password'])

"""------------MEMBER-------------"""
@member_ns.route('')
class MemberList(Resource):
    @member_ns.doc(
        security='jwt',
        description='Lấy danh sách tất cả thành viên',
        responses={200: 'Thành công'}
    )
    @cache.cached(timeout=60)
    def get(self):
        """Lấy tất cả thành viên (Read All)"""
        return MemberService.get_all_members()

    @member_ns.doc(
        security='jwt',
        description='Thêm một thành viên mới',
        responses={
            201: 'Thông tin được tạo thành công',
            400: 'Thiếu dữ liệu',
            401: 'Chưa được xác thực',
            409: 'Số điện thoại đã tồn tại'
        }
    )
    @member_ns.expect(member_model, validate=True)
    @jwt_required()
    def post(self):
        """Thêm thành viên mới (Create)"""
        data = self.api.payload
        return MemberService.create_member(data)

@member_ns.route('/<int:member_id>')
@member_ns.param('member_id', 'Định danh thành viên')
class MemberItem(Resource):
    @member_ns.doc(description='Lấy thông tin thành viên theo ID')
    @cache.cached(timeout=120)
    def get(self, member_id):
        """Lấy thông tin thành viên theo ID (Read One)"""
        return MemberService.get_member_by_id(member_id)

    @member_ns.doc(description='Cập nhật thông tin thành viên')
    @member_ns.expect(member_model)
    @jwt_required()
    def put(self, member_id):
        """Cập nhật thông tin thành viên (Update)"""
        data = api.payload
        return MemberService.update_member(member_id, data)

    @member_ns.doc(description='Xóa thông tin thành viên')
    @jwt_required()
    def delete(self, member_id):
        """Xóa thành viên (Delete)"""
        return MemberService.delete_member(member_id)

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
        return BookService.get_all_books()

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
        data = self.api.payload
        return BookService.create_book(data)

@book_ns.route('/<int:book_id>')
@book_ns.param('book_id', 'Định danh của cuốn sách')
class BookItem(Resource):
    @book_ns.doc(description='Lấy thông tin sách theo ID')
    @cache.cached(timeout=120)
    def get(self, book_id):
        """Lấy thông tin sách theo ID (Read One)"""
        return BookService.get_book_by_id(book_id)

    @book_ns.doc(description='Cập nhật thông tin sách')
    @book_ns.expect(book_model)
    @jwt_required()
    def put(self, book_id):
        """Cập nhật thông tin sách (Update)"""
        data = api.payload
        return BookService.update_book(book_id, data)

    @book_ns.doc(description='Xóa sách')
    @jwt_required()
    def delete(self, book_id):
        """Xóa sách (Delete)"""
        return BookService.delete_book(book_id)

"""------------TRANSACTION---------------"""
@transaction_ns.route('/<int:book_id>')
@transaction_ns.param('book_id', 'ID sách')
@transaction_ns.param('member_id', 'ID thành viên')
class Transaction_User(Resource):
    @book_ns.doc(description='Tạo giao dịch mượn sách')
    @jwt_required()
    def post(self, book_id, member_id):
        """Tạo giao dịch mượn sách"""
        return TransactionService.borrow_book(book_id, member_id)

    @book_ns.doc(description='Hoàn tất giao dịch (trả sách)')
    @jwt_required()
    def delete(self, book_id, member_id):
        """Hoàn tất giao dịch (trả sách)"""
        return TransactionService.return_book(book_id, member_id)


if __name__ == '__main__':
    app.run(debug=True)

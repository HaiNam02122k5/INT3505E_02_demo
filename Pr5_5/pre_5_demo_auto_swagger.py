from flask import Flask
from flask_restx import Api, Resource, fields

from models import db, Book

app = Flask(__name__)

# --- Cấu hình database ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# --- Cấu hình Swagger tự động ---
api = Api(
    app,
    version="1.0",
    title="Book Management API",
    description="Tài liệu API tự động sinh bằng Flask-RESTX",
    doc="/docs/",
)

book_ns = api.namespace("Books", path="/api/books", description="CRUD operations for books")

# --- Mô hình dữ liệu Swagger ---
book_model = api.model('Book', {
    'id': fields.Integer(readonly=True, description='Book ID'),
    'title': fields.String(required=True, description='Book title'),
    'author': fields.String(required=True, description='Book author'),
    'year': fields.Integer(description='Published year'),
    'genre': fields.String(description='Book genre')
})

with app.app_context():
    db.create_all()

# --- CRUD Endpoints ---
@book_ns.route('/')
class BookList(Resource):
    @book_ns.marshal_list_with(book_model)
    def get(self):
        """Lấy danh sách tất cả sách"""
        return Book.query.all()

    @book_ns.expect(book_model)
    @book_ns.marshal_with(book_model, code=201)
    def post(self):
        """Thêm một cuốn sách mới"""
        data = api.payload
        book = Book(title=data['title'], author=data['author'],
                    year=data.get('year'), genre=data.get('genre'))
        db.session.add(book)
        db.session.commit()
        return book, 201


@book_ns.route('/<int:book_id>')
@book_ns.response(404, 'Book not found')
@book_ns.param('book_id', 'ID của sách')
class BookResource(Resource):
    @book_ns.marshal_with(book_model)
    def get(self, book_id):
        """Lấy thông tin một cuốn sách"""
        book = Book.query.get(book_id)
        if not book:
            api.abort(404, "Book not found")
        return book

    @book_ns.expect(book_model)
    @book_ns.marshal_with(book_model)
    def put(self, book_id):
        """Cập nhật thông tin sách"""
        book = Book.query.get(book_id)
        if not book:
            api.abort(404, "Book not found")
        data = api.payload
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.year = data.get('year', book.year)
        book.genre = data.get('genre', book.genre)
        db.session.commit()
        return book

    @book_ns.response(204, 'Deleted')
    def delete(self, book_id):
        """Xóa một cuốn sách"""
        book = Book.query.get(book_id)
        if not book:
            api.abort(404, "Book not found")
        db.session.delete(book)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)

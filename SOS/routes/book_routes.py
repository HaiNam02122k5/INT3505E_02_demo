from flask_restx import Resource
from flask_jwt_extended import jwt_required

from SOS.extensions import cache
from SOS.services import BookService

def init_book_routes(api, book_ns, schemas):
    """Khởi tạo các route cho sách"""

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
        @book_ns.expect(schemas['book'], validate=True) # Yêu cầu đầu vào phải theo book_model
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
        @book_ns.expect(schemas['book'])
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
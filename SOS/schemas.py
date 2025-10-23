from flask_restx import fields

def init_schemas(api):
    """Khởi tạo các schema cho Swagger"""
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

    token_model = api.model('Token', {
        'access_token': fields.String(description='JWT Access Token')
    })

    return {
        'login': login_model,
        'book': book_model,
        'member': member_model,
        'token': token_model
    }
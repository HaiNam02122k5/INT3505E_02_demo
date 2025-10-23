from datetime import timedelta

from flask import Flask
from flask_restx import Api

from SOS.extensions import jwt, db, cache
from SOS.models import User
from SOS.schemas import init_schemas
from SOS.routes import init_member_routes, init_transaction_routes, init_book_routes, init_user_routes

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
transaction_ns = api.namespace("Transactions", path="/api", description="CRUD operations for transactions")
member_ns = api.namespace("Member", path="/api/members", description="CRUD operations for members")

db.init_app(app)
jwt.init_app(app)
cache.init_app(app)

# Khởi tạo schemas
schemas = init_schemas(api)

# Khởi tạo route
init_user_routes(api, user_ns, schemas)
init_member_routes(api, member_ns, schemas)
init_book_routes(api, book_ns, schemas)
init_transaction_routes(transaction_ns)

with app.app_context():
    db.create_all()
    if not User.query.first():
        admin_user = User(username='admin', password='12345678')
        db.session.add(admin_user)
        db.session.commit()

@app.route('/api/')
def start():
    return "Chào mừng đến với Thư Viện!"

if __name__ == '__main__':
    app.run(debug=True)

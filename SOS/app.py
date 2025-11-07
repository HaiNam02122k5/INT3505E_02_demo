from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from SOS.config import Config
from SOS.extensions import jwt, db, cache
from SOS.routes import init_member_routes, init_transaction_routes, init_book_routes, init_user_routes
from SOS.schemas import init_schemas


def create_app():
    # Khởi tạo ứng dụng Flask
    app = Flask(__name__)

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    app.config.from_object(Config)

    api = Api(
        app,
        version="1.0",
        title="Book Management API",
        description="Tài liệu API tự động sinh bằng Flask-RESTX",
        doc="/docs/",
        security='jwt', # Mặc định bảo vệ tất cả endpoint
        authorizations=Config.AUTHORIZATIONS # Định nghĩa cách thức bảo vệ
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

    @app.route('/api/')
    def start():
        return "Chào mừng đến với Thư Viện!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

import pytest
from SOS.app import create_app
from SOS.extensions import db
from SOS.models.user import User
from SOS.models.book import Book
from SOS.models.member import Member
from SOS.models.transaction import Transaction
from flask_jwt_extended import create_access_token


@pytest.fixture(scope='session')
def app():
    """Tạo Flask app cho testing"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'tests-secret-key',
        'CACHE_TYPE': 'SimpleCache',
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """CLI runner"""
    return app.test_cli_runner()


# @pytest.fixture(scope='function')
# def db_session(app):
#     """Database session cho mỗi tests"""
#     with app.app_context():
#         connection = db.engine.connect()
#         transaction = connection.begin()
#
#         # Bind session to connection
#         session = db.create_scoped_session(
#             options={'bind': connection, 'binds': {}}
#         )
#         db.session = session
#
#         yield session
#
#         session.close()
#         transaction.rollback()
#         connection.close()

@pytest.fixture(scope='function')
def db_session(app):
    """
    Database session cho mỗi tests.
    Chiến lược này sẽ "dọn dẹp" (xóa) toàn bộ dữ liệu
    sau mỗi test thay vì dùng nested transaction.
    """
    with app.app_context():
        # Bàn giao session cho test case
        yield db.session

        # --- Dọn dẹp sau khi test chạy xong ---

        # 1. Gỡ bỏ session hiện tại để giải phóng mọi kết nối
        db.session.remove()

        # 2. XÓA SỔ tất cả các bảng
        db.drop_all()

        # 3. TẠO LẠI tất cả các bảng
        # (Để test case tiếp theo có cái để chạy)
        db.create_all()

@pytest.fixture
def test_user(db_session):
    """Tạo user tests"""
    user = User(
        username='testuser',
        password='testpass123',
        name='Test User'
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def auth_token(app, test_user):
    """Tạo JWT token cho tests"""
    with app.app_context():
        token = create_access_token(identity=str(test_user.id))
    return token


@pytest.fixture
def auth_headers(auth_token):
    """Headers với JWT token"""
    return {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_book(db_session):
    """Tạo sách mẫu"""
    book = Book(
        title='Test Book',
        author='Test Author',
        isbn='1234567890',
        copies=5
    )
    db_session.add(book)
    db_session.commit()
    return book


@pytest.fixture
def sample_member(db_session):
    """Tạo thành viên mẫu"""
    member = Member(
        name='Test Member',
        phone_number='0123456789',
        address='Test Address'
    )
    db_session.add(member)
    db_session.commit()
    return member


@pytest.fixture
def sample_transaction(db_session, sample_book, sample_member):
    """Tạo giao dịch mẫu"""
    transaction = Transaction(
        book_id=sample_book.id,
        member_id=sample_member.id
    )
    db_session.add(transaction)
    sample_book.copies -= 1
    db_session.commit()
    return transaction

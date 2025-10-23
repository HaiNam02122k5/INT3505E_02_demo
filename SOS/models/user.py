from SOS.extensions import db

class User(db.Model):
    """Mô hình người dùng đơn giản cho mục đích minh họa"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phoneNumber = db.Column(db.String(10), nullable=True)


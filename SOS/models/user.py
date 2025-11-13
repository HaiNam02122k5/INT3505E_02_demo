from SOS.extensions import db

class User(db.Model):
    """Mô hình người dùng đơn giản cho mục đích minh họa"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(10), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name if self.name else None,
            'username': self.username,
            'phone_number': self.phone_number if self.phone_number else None
        }


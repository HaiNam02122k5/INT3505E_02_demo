from SOS.extensions import db

class Member(db.Model):
    """Mô hình thành viên đơn giản cho mục đích minh họa"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'phone': self.phone_number,
            'address': self.address
        }
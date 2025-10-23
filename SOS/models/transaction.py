from datetime import datetime

from SOS.extensions import db

class Transaction(db.Model):
    """Mô hình cho Giao dịch Mượn/Trả"""
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)  # None nếu chưa được trả

    member = db.relationship('Member', backref=db.backref('transactions', lazy=True))
    book = db.relationship('Book', backref=db.backref('transactions', lazy=True))

    def to_dict(self):
        """Chuyển đổi đối tượng Transaction sang dictionary để trả về JSON"""
        return {
            'id': self.id,
            'book_id': self.book_id,
            'book_title': self.book.title,
            'member_id': self.member_id,
            'member_name': self.member.name,
            'borrow_date': self.borrow_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None
        }
from SOS.extensions import db

class Book(db.Model):
    """Mô hình cho Sách"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    copies = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Chuyển đổi đối tượng Book sang dictionary để trả về JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'copies': self.copies
        }
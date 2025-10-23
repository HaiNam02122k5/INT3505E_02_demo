from datetime import datetime

from SOS.extensions import db, cache
from SOS.models.book import Book
from SOS.models.member import Member
from SOS.models.transaction import Transaction


class TransactionService:
    @staticmethod
    def get_transactions_by_member_id(member_id):
        transactions = Transaction.query.filter_by(member_id=member_id).all()
        return [transaction.to_dict() for transaction in transactions]


    @staticmethod
    def borrow_book(book_id, member_id, borrow_date=None):
        """Mượn sách"""
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Không tìm thấy sách với ID này.'}, 404

        if book.copies <= 0:
            return {'message': 'Sách hiện đã được mượn hết.'}, 409

        member = Member.query.get(member_id)
        if not member:
            return {'message': f'Không tìm thấy thành viên có ID {member_id}'}, 404

        new_transaction = Transaction(
            book_id=book.id,
            member_id=int(member_id)
        )

        try:
            db.session.add(new_transaction)
            book.copies = book.copies - 1
            cache.clear()
            db.session.commit()
            return {'message': 'Mượn sách thành công', 'transaction': new_transaction.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi khi mượn sách: {e}'}, 500

    @staticmethod
    def return_book(book_id, member_id):
        """Trả sách"""
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Không tìm thấy sách với ID này.'}, 404

        transaction = Transaction.query.filter_by(
            book_id=book_id,
            member_id=int(member_id),
            return_date=None
        ).first()

        if not transaction:
            return {'message': 'Không tìm thấy giao dịch mở cho sách này của bạn.'}, 404

        try:
            transaction.return_date = datetime.utcnow()
            book.copies = book.copies + 1
            cache.clear()
            db.session.commit()
            return {'message': 'Trả sách thành công', 'transaction': transaction.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi khi trả sách: {e}'}, 500
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from SOS.services import TransactionService

def init_transaction_routes(transaction_ns):
    """Khởi tạo các route cho Giao dịch"""

    @transaction_ns.route('/members/<int:member_id>/transactions')
    @transaction_ns.param('member_id', 'ID thành viên')
    class MemberTransaction(Resource):
        @transaction_ns.doc(description='Lấy tất cả giao dịch của 1 thành viên')
        def get(self, member_id):
            return TransactionService.get_transactions_by_member_id(member_id)

    @transaction_ns.route('/members/<int:member_id>/transactions/<int:book_id>')
    @transaction_ns.param('book_id', 'ID sách')
    @transaction_ns.param('member_id', 'ID thành viên')
    class Transaction(Resource):
        @transaction_ns.doc(description='Tạo giao dịch mượn sách')
        @jwt_required()
        def post(self, book_id, member_id):
            """Tạo giao dịch mượn sách"""
            return TransactionService.borrow_book(book_id, member_id)

        @transaction_ns.doc(description='Hoàn tất giao dịch (trả sách)')
        @jwt_required()
        def delete(self, book_id, member_id):
            """Hoàn tất giao dịch (trả sách)"""
            return TransactionService.return_book(book_id, member_id)
import pytest
from datetime import datetime
from SOS.services.transaction_service import TransactionService
from SOS.models.transaction import Transaction


@pytest.mark.unit
class TestTransactionService:
    """Test TransactionService methods"""

    def test_get_transactions_by_member_empty(self, db_session, sample_member):
        """Test lấy giao dịch của thành viên chưa có giao dịch"""
        result = TransactionService.get_transactions_by_member_id(sample_member.id)
        assert result == []

    def test_get_transactions_by_member_with_data(self, db_session, sample_transaction):
        """Test lấy giao dịch của thành viên có giao dịch"""
        result = TransactionService.get_transactions_by_member_id(
            sample_transaction.member_id
        )
        assert len(result) == 1
        assert result[0]['book_id'] == sample_transaction.book_id

    def test_borrow_book_success(self, db_session, sample_book, sample_member):
        """Test mượn sách thành công"""
        initial_copies = sample_book.copies

        result, status = TransactionService.borrow_book(
            sample_book.id,
            sample_member.id
        )

        assert status == 201
        assert result['message'] == 'Mượn sách thành công'

        # Verify copies decreased
        db_session.refresh(sample_book)
        assert sample_book.copies == initial_copies - 1

    def test_borrow_book_not_available(self, db_session, sample_book, sample_member):
        """Test mượn sách khi hết"""
        sample_book.copies = 0
        db_session.commit()

        result, status = TransactionService.borrow_book(
            sample_book.id,
            sample_member.id
        )

        assert status == 409
        assert 'hết' in result['message'].lower()

    def test_borrow_book_invalid_book(self, db_session, sample_member):
        """Test mượn sách không tồn tại"""
        result, status = TransactionService.borrow_book(999, sample_member.id)
        assert status == 404
        assert 'Không tìm thấy sách' in result['message']

    def test_borrow_book_invalid_member(self, db_session, sample_book):
        """Test mượn sách với thành viên không tồn tại"""
        result, status = TransactionService.borrow_book(sample_book.id, 999)
        assert status == 404
        assert 'Không tìm thấy thành viên' in result['message']

    def test_return_book_success(self, db_session, sample_transaction, sample_book):
        """Test trả sách thành công"""
        initial_copies = sample_book.copies

        result, status = TransactionService.return_book(
            sample_transaction.book_id,
            sample_transaction.member_id
        )

        assert status == 200
        assert result['message'] == 'Trả sách thành công'

        # Verify copies increased
        db_session.refresh(sample_book)
        assert sample_book.copies == initial_copies + 1

        # Verify return date is set
        db_session.refresh(sample_transaction)
        assert sample_transaction.return_date is not None

    def test_return_book_no_active_transaction(self, db_session, sample_book, sample_member):
        """Test trả sách khi không có giao dịch mở"""
        result, status = TransactionService.return_book(
            sample_book.id,
            sample_member.id
        )

        assert status == 404
        assert 'Không tìm thấy giao dịch' in result['message']

    def test_return_book_already_returned(self, db_session, sample_transaction):
        """Test trả sách đã được trả"""
        # Return once
        sample_transaction.return_date = datetime.utcnow()
        db_session.commit()

        # Try to return again
        result, status = TransactionService.return_book(
            sample_transaction.book_id,
            sample_transaction.member_id
        )

        assert status == 404
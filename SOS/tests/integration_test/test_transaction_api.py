import pytest
import json


@pytest.mark.integration
class TestTransactionAPI:
    """Test Transaction API endpoints"""

    def test_borrow_book_flow(self, client, auth_headers, sample_book, sample_member):
        """Test luồng mượn sách hoàn chỉnh"""
        # 1. Get initial book copies
        response = client.get(f'/api/books/{sample_book.id}')
        initial_data = json.loads(response.data)
        initial_copies = initial_data['copies']

        # 2. Borrow book
        response = client.post(
            f'/api/members/{sample_member.id}/transactions/{sample_book.id}',
            headers=auth_headers
        )
        assert response.status_code == 201

        # 3. Verify copies decreased
        response = client.get(f'/api/books/{sample_book.id}')
        updated_data = json.loads(response.data)
        assert updated_data['copies'] == initial_copies - 1

        # 4. Get transactions
        response = client.get(
            f'/api/members/{sample_member.id}/transactions',
            headers=auth_headers
        )
        assert response.status_code == 200
        transactions = json.loads(response.data)
        assert len(transactions) > 0

    def test_return_book_flow(self, client, auth_headers, sample_transaction, sample_book):
        """Test luồng trả sách hoàn chỉnh"""
        # 1. Get initial book copies
        response = client.get(f'/api/books/{sample_book.id}')
        initial_data = json.loads(response.data)
        initial_copies = initial_data['copies']

        # 2. Return book
        response = client.delete(
            f'/api/members/{sample_transaction.member_id}/transactions/{sample_transaction.book_id}',
            headers=auth_headers
        )
        assert response.status_code == 200

        # 3. Verify copies increased
        response = client.get(f'/api/books/{sample_book.id}')
        updated_data = json.loads(response.data)
        assert updated_data['copies'] == initial_copies + 1

    def test_borrow_unavailable_book(self, client, auth_headers, sample_book, sample_member):
        """Test mượn sách đã hết"""
        # Set copies to 0
        sample_book.copies = 0
        from SOS.extensions import db
        db.session.commit()

        response = client.post(
            f'/api/members/{sample_member.id}/transactions/{sample_book.id}',
            headers=auth_headers
        )

        assert response.status_code == 409

    def test_multiple_borrows_same_member(self, client, auth_headers, db_session, sample_member):
        """Test một thành viên mượn nhiều sách"""
        from SOS.models.book import Book

        # Create multiple books
        books = []
        for i in range(3):
            book = Book(
                title=f'Book {i}',
                author=f'Author {i}',
                isbn=f'ISBN{i:010d}',
                copies=5
            )
            db_session.add(book)
            books.append(book)
        db_session.commit()

        # Borrow all books
        for book in books:
            response = client.post(
                f'/api/members/{sample_member.id}/transactions/{book.id}',
                headers=auth_headers
            )
            assert response.status_code == 201

        # Verify all transactions
        response = client.get(
            f'/api/members/{sample_member.id}/transactions',
            headers=auth_headers
        )
        transactions = json.loads(response.data)
        assert len(transactions) == 3

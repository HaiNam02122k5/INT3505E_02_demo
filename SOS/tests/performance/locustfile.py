from locust import HttpUser, task, between, SequentialTaskSet
import random
import json


class LibraryUserBehavior(SequentialTaskSet):
    """Mô phỏng hành vi người dùng thực tế"""

    def on_start(self):
        """Setup - Login và lấy token"""
        response = self.client.post("/api/users",
                                    json={
                                        "username": "admin",
                                        "password": "12345678"
                                    }
                                    )
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('access_token')
            self.headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
        else:
            self.token = None
            self.headers = {}

    @task(10)
    def browse_books(self):
        """Task: Xem danh sách sách (thường xuyên nhất)"""
        self.client.get("/api/books", headers=self.headers)

    @task(8)
    def view_book_detail(self):
        """Task: Xem chi tiết sách"""
        book_id = random.randint(1, 100)  # Giả sử có 100 sách
        self.client.get(f"/api/books/{book_id}", headers=self.headers)

    @task(5)
    def browse_members(self):
        """Task: Xem danh sách thành viên"""
        self.client.get("/api/members", headers=self.headers)

    @task(3)
    def create_book(self):
        """Task: Thêm sách mới"""
        if not self.token:
            return

        data = {
            "title": f"Performance Test Book {random.randint(1, 10000)}",
            "author": f"Author {random.randint(1, 1000)}",
            "isbn": f"{random.randint(1000000000, 9999999999)}",
            "copies": random.randint(1, 10)
        }
        self.client.post("/api/books",
                         json=data,
                         headers=self.headers)

    @task(2)
    def create_member(self):
        """Task: Thêm thành viên mới"""
        if not self.token:
            return

        data = {
            "name": f"Member {random.randint(1, 10000)}",
            "phone_number": f"09{random.randint(10000000, 99999999)}",
            "address": f"Address {random.randint(1, 1000)}"
        }
        self.client.post("/api/members",
                         json=data,
                         headers=self.headers)

    @task(4)
    def borrow_book(self):
        """Task: Mượn sách"""
        if not self.token:
            return

        member_id = random.randint(1, 50)
        book_id = random.randint(1, 100)

        self.client.post(f"/api/members/{member_id}/transactions/{book_id}",
                         headers=self.headers)

    @task(2)
    def view_transactions(self):
        """Task: Xem lịch sử mượn/trả"""
        member_id = random.randint(1, 50)
        self.client.get(f"/api/members/{member_id}/transactions",
                        headers=self.headers)


class LibraryUser(HttpUser):
    """Định nghĩa user cho load test"""
    tasks = [LibraryUserBehavior]
    wait_time = between(1, 3)  # Đợi 1-3 giây giữa các task


class StressTestUser(HttpUser):
    """User cho stress test - không có wait time"""
    tasks = [LibraryUserBehavior]
    wait_time = between(0.1, 0.5)  # Đợi rất ngắn
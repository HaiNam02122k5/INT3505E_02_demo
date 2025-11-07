import pytest
from SOS.services.member_service import MemberService
from SOS.models.member import Member


@pytest.mark.unit
class TestMemberService:
    """Test MemberService methods"""

    def test_get_all_members_empty(self, db_session):
        """Test lấy danh sách thành viên khi trống"""
        result, status = MemberService.get_all_members()
        assert status == 200
        assert result == []

    def test_get_all_members_with_data(self, db_session, sample_member):
        """Test lấy danh sách thành viên có dữ liệu"""
        result, status = MemberService.get_all_members()
        assert status == 200
        assert len(result) == 1
        assert result[0]['name'] == 'Test Member'

    def test_get_member_by_id_success(self, db_session, sample_member):
        """Test lấy thành viên theo ID thành công"""
        result, status = MemberService.get_member_by_id(sample_member.id)
        assert status == 200
        assert result['name'] == 'Test Member'
        assert result['phone'] == '0123456789'

    def test_get_member_by_id_not_found(self, db_session):
        """Test lấy thành viên không tồn tại"""
        result, status = MemberService.get_member_by_id(999)
        assert status == 404

    def test_create_member_success(self, db_session):
        """Test tạo thành viên mới thành công"""
        data = {
            'name': 'New Member',
            'phone_number': '0987654321',
            'address': 'New Address'
        }
        result, status = MemberService.create_member(data)
        assert status == 201
        assert result['message'] == 'Thêm thành viên thành công'
        assert result['member']['name'] == 'New Member'

    def test_create_member_duplicate_phone(self, db_session, sample_member):
        """Test tạo thành viên với SĐT trùng"""
        data = {
            'name': 'Another Member',
            'phone_number': '0123456789',  # Trùng SĐT
            'address': 'Another Address'
        }
        result, status = MemberService.create_member(data)
        assert status == 409
        assert 'Số điện thoại đã tồn tại' in result['message']

    def test_update_member_success(self, db_session, sample_member):
        """Test cập nhật thành viên thành công"""
        data = {
            'name': 'Updated Name',
            'address': 'Updated Address'
        }
        result, status = MemberService.update_member(sample_member.id, data)
        assert status == 200
        assert result['member']['name'] == 'Updated Name'

    def test_update_member_not_found(self, db_session):
        """Test cập nhật thành viên không tồn tại"""
        data = {'name': 'Updated Name'}
        result, status = MemberService.update_member(999, data)
        assert status == 404

    def test_delete_member_success(self, db_session, sample_member):
        """Test xóa thành viên thành công"""
        member_id = sample_member.id
        result, status = MemberService.delete_member(member_id)
        assert status == 200

        # Verify member is deleted
        member = Member.query.get(member_id)
        assert member is None

    def test_delete_member_not_found(self, db_session):
        """Test xóa thành viên không tồn tại"""
        result, status = MemberService.delete_member(999)
        assert status == 404

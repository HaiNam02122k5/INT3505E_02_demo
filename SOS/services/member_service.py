from SOS.extensions import db, cache
from SOS.models.member import Member

class MemberService:
    @staticmethod
    def get_all_members():
        """Lấy tất cả thành viên"""
        members = Member.query.all()
        return [member.to_dict() for member in members], 200

    @staticmethod
    def get_member_by_id(member_id):
        """Lấy thông tin thành viên theo ID"""
        member = Member.query.get(member_id)
        if not member:
            return {'message': 'Không tìm thấy thành viên.'}, 404
        return member.to_dict(), 200

    @staticmethod
    def create_member(data):
        """Thêm thành viên mới"""
        if Member.query.filter_by(phone_number=data['phone_number']).first():
            return {'message': 'Số điện thoại đã tồn tại.'}, 409

        new_member = Member(
            name=data['name'],
            phone_number=data['phone_number'],
            address=data['address']
        )

        try:
            db.session.add(new_member)
            cache.clear()
            db.session.commit()
            return {'message': 'Thêm thành viên thành công', 'member': new_member.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi DB: {e}'}, 500

    @staticmethod
    def update_member(book_id, data):
        """Cập nhật thông tin thành viên"""
        member = Member.query.get(book_id)
        if not member:
            return {'message': 'Không tìm thấy thành viên.'}, 404

        try:
            member.name = data.get('name', member.name)
            member.phone_number = data.get('phone_number', member.phone_number)
            member.address = data.get('address', member.address)

            cache.clear()
            db.session.commit()
            return {'message': 'Cập nhật thành công', 'member': member.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi khi cập nhật thông tin thành viên: {e}'}, 500

    @staticmethod
    def delete_member(member_id):
        """Xóa thành viên"""
        member = Member.query.get(member_id)
        if not member:
            return {'message': 'Không tìm thấy thành viên.'}, 404

        try:
            db.session.delete(member)
            cache.clear()
            db.session.commit()
            return {'message': 'Xóa thông tin thành viên thành công.'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Lỗi khi xóa thành viên: {e}'}, 500
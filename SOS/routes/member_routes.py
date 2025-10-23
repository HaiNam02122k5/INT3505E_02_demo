from flask_restx import Resource
from flask_jwt_extended import jwt_required

from SOS.extensions import cache
from SOS.services import MemberService

def init_member_routes(api, member_ns, schemas):
    """Khởi tạo các route cho thành viên"""

    @member_ns.route('')
    class MemberList(Resource):
        @member_ns.doc(
            security='jwt',
            description='Lấy danh sách tất cả thành viên',
            responses={200: 'Thành công'}
        )
        @cache.cached(timeout=60)
        def get(self):
            """Lấy tất cả thành viên (Read All)"""
            return MemberService.get_all_members()

        @member_ns.doc(
            security='jwt',
            description='Thêm một thành viên mới',
            responses={
                201: 'Thông tin được tạo thành công',
                400: 'Thiếu dữ liệu',
                401: 'Chưa được xác thực',
                409: 'Số điện thoại đã tồn tại'
            }
        )
        @member_ns.expect(schemas['member'], validate=True)
        @jwt_required()
        def post(self):
            """Thêm thành viên mới (Create)"""
            data = self.api.payload
            return MemberService.create_member(data)

    @member_ns.route('/<int:member_id>')
    @member_ns.param('member_id', 'Định danh thành viên')
    class MemberItem(Resource):
        @member_ns.doc(description='Lấy thông tin thành viên theo ID')
        @cache.cached(timeout=120)
        def get(self, member_id):
            """Lấy thông tin thành viên theo ID (Read One)"""
            return MemberService.get_member_by_id(member_id)

        @member_ns.doc(description='Cập nhật thông tin thành viên')
        @member_ns.expect(schemas['member'])
        @jwt_required()
        def put(self, member_id):
            """Cập nhật thông tin thành viên (Update)"""
            data = api.payload
            return MemberService.update_member(member_id, data)

        @member_ns.doc(description='Xóa thông tin thành viên')
        @jwt_required()
        def delete(self, member_id):
            """Xóa thành viên (Delete)"""
            return MemberService.delete_member(member_id)
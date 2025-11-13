from flask import Blueprint, request, jsonify

# Tạo một Blueprint cho v1
bp_v1 = Blueprint('v1', __name__)


@bp_v1.route('/payments', methods=['POST'])
def process_payment():
    data = request.get_json()
    amount = data.get('amount')

    # Logic cũ: Không cần check currency, mặc định là VND
    response = {
        "status": "success",
        "version": "v1 (Old)",
        "message": f"Đã thanh toán {amount} VND.",
        "data": {
            "amount": amount,
            "currency": "VND"
        }
    }

    # --- LIFECYCLE MANAGEMENT ---
    # Thêm header cảnh báo người dùng sắp ngừng hỗ trợ v1
    headers = {
        "Warning": '299 - "This API version is deprecated. Please migrate to v2."'
    }

    return jsonify(response), 200, headers
from flask import Blueprint, request, jsonify

# Tạo một Blueprint cho v2
bp_v2 = Blueprint('v2', __name__)


@bp_v2.route('/payments', methods=['POST'])
def process_payment():
    data = request.get_json()
    amount = data.get('amount')
    currency = data.get('currency')  # Trường mới

    # --- VALIDATION (Breaking Change) ---
    # v2 bắt buộc phải có currency
    if not currency:
        return jsonify({
            "status": "error",
            "version": "v2",
            "message": "Lỗi: Thiếu trường 'currency'. v2 yêu cầu mã tiền tệ (USD, EUR, VND...)"
        }), 400

    # Logic mới xử lý đa tiền tệ
    response = {
        "status": "success",
        "version": "v2 (New)",
        "message": f"Đã thanh toán {amount} {currency} thành công.",
        "transaction_id": "TRANS_9999",  # v2 trả về thêm ID giao dịch
        "data": {
            "amount": amount,
            "currency": currency
        }
    }

    return jsonify(response), 200
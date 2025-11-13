from flask import Flask
from routes.payment_v1 import bp_v1
from routes.payment_v2 import bp_v2

app = Flask(__name__)

# Đăng ký các Blueprint với tiền tố URL (URL Prefix)
# Đây là kỹ thuật "URL Path Versioning"
app.register_blueprint(bp_v1, url_prefix='/api/v1')
app.register_blueprint(bp_v2, url_prefix='/api/v2')

@app.route('/')
def index():
    return "Payment API Gateway is running..."

if __name__ == '__main__':
    # Chạy server ở port 5000
    app.run(debug=True, port=5000)
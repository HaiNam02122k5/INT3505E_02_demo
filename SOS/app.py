from flask import Flask

app = Flask(__name__)

@app.route('/api/')
def start():
    return "Chào mừng đến với Thư Viện!"

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home_page():
    return jsonify({'message': 'home page'})

@app.route('/login')
def login_page():
    return jsonify({'message': 'login here'})

@app.route('/signup')
def signup_page():
    return jsonify({'message': 'signup here'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

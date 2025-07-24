# app.py
from flask import Flask
from routes import register_routes
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)

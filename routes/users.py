from flask import Blueprint, request, jsonify
from utils.security import hash_password, verify_password
from utils.validators import is_valid_email

users_bp = Blueprint('users', __name__)
from db import get_connection
import re

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def health_check():
    return jsonify({"message": "User Management System is up"}), 200

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(user) for user in users]), 200

@users_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify(dict(user)), 200
    else:
        return jsonify({"error": "User not found"}), 404


@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return "Missing fields", 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email", 400

    if len(password) < 8:
        return "Password must be at least 8 characters", 400

    hashed_password = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    # Check for duplicate email
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        return "Email already exists", 409

    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                   (name, email, hashed_password))
    conn.commit()
    conn.close()

    return "User created successfully", 201

@users_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Missing fields"}), 400

    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User updated successfully"}), 200

@users_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

@users_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f'%{name}%',))
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(user) for user in users]), 200

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user and verify_password(password, user['password']):
        return jsonify({"status": "success", "user_id": user['id']}), 200
    else:
        return jsonify({"status": "failed", "message": "Invalid credentials"}), 401

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

fake_users = {
    "user@example.com": generate_password_hash("senha123")
}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email in fake_users and check_password_hash(fake_users[email], password):
        return jsonify({"token": "fake-token-for-" + email})
    return jsonify({"error": "Login inválido"}), 401

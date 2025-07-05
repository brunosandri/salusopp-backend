from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json

# ---------- carregar usuários do JSON ----------
with open("usuarios.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

usuarios = {
    email: generate_password_hash(dados["senha"])
    for email, dados in raw_data.items()
}

# ---------- criar Blueprint ----------
auth_bp = Blueprint("auth", __name__)

# ---------- rota de login ----------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    senha = data.get("password")

    # valida
    if email in usuarios and check_password_hash(usuarios[email], senha):
        return jsonify({"token": f"fake-token-for-{email}"})
    return jsonify({"error": "Login inválido"}), 401

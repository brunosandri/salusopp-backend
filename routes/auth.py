import json
from werkzeug.security import generate_password_hash, check_password_hash

with open("usuarios.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

usuarios = {
    email: generate_password_hash(dados["senha"])
    for email, dados in raw_data.items()
}

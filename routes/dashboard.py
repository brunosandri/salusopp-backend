
import os
import json
import shutil
from datetime import datetime
from flask import Blueprint, jsonify, request

dashboard_bp = Blueprint('dashboard', __name__)

with open("nfts.json", "r", encoding="utf-8") as f:
    nft_data = json.load(f)

ARQUIVO_ETAPAS = "etapas_obra.json"
BACKUP_DIR = "backups"

def carregar_etapas():
    try:
        with open(ARQUIVO_ETAPAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def criar_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"etapas_{timestamp}.json")
    shutil.copy(ARQUIVO_ETAPAS, backup_path)

@dashboard_bp.route("/nfts/<email>", methods=["GET"])
def get_nfts(email):
    email = email.lower()
    return jsonify(nft_data.get(email, []))

@dashboard_bp.route('/obra', methods=['GET'])
def get_status_obra():
    return jsonify(carregar_etapas())

@dashboard_bp.route('/adicionar-etapa', methods=['POST'])
def adicionar_etapa():
    nova_etapa = request.json
    etapas = carregar_etapas()
    etapas.append(nova_etapa)

    # Salvar e criar backup
    with open(ARQUIVO_ETAPAS, "w", encoding="utf-8") as f:
        json.dump(etapas, f, indent=2, ensure_ascii=False)
    criar_backup()

    return "Etapa adicionada com sucesso", 200

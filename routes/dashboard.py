
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
BASE_DIR = os.path.dirname(__file__)
NFTS_FILE = os.path.join(BASE_DIR, "../data/nfts.json")
DOCUMENTOS_FILE = os.path.join(BASE_DIR, "../data/documentos.json")

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
def get_nfts_por_email(email):
    try:
        with open(NFTS_FILE, "r") as f:
            nfts = json.load(f)
        nfts_usuario = [n for n in nfts if n["email"] == email]
        return jsonify(nfts_usuario)
    except Exception as e:
        return jsonify({"erro": "Falha ao carregar NFTs", "detalhe": str(e)}), 500


@dashboard_bp.route('/obra', methods=['GET'])
def get_status_obra():
    return jsonify(carregar_etapas())

@dashboard_bp.route('/adicionar-etapa', methods=['POST'])
def adicionar_etapa():
    nova_etapa = request.json
    etapas = carregar_etapas()
    etapas.append(nova_etapa)

@dashboard_bp.route("/documentos/<email>", methods=["GET"])
def get_documentos(email):
    try:
        with open(DOCUMENTOS_FILE, "r") as f:
            documentos = json.load(f)

        docs_gerais = [doc for doc in documentos if doc["email"] == "geral"]
        docs_usuario = [doc for doc in documentos if doc["email"] == email]

        return jsonify(docs_gerais + docs_usuario)
    except Exception as e:
        return jsonify({"erro": "Falha ao carregar documentos", "detalhe": str(e)}), 500

    # Salvar e criar backup
    with open(ARQUIVO_ETAPAS, "w", encoding="utf-8") as f:
        json.dump(etapas, f, indent=2, ensure_ascii=False)
    criar_backup()

    return "Etapa adicionada com sucesso", 200

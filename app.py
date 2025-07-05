
from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.uploads import uploads_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "salusopp")
app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER", "uploads")

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(uploads_bp)

# Rota para servir arquivos da pasta de documentos
from flask import send_from_directory

@app.route('/uploads/<user_id>/<filename>')
def download_file(user_id, filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    return send_from_directory(path, filename)

# Rota para upload de documentos
@app.route('/upload-doc/<email>', methods=['POST'])
def upload_doc(email):
    from flask import request
    if 'file' not in request.files:
        return "Arquivo ausente", 400
    file = request.files['file']
    pasta_destino = os.path.join(app.config['UPLOAD_FOLDER'], email)
    os.makedirs(pasta_destino, exist_ok=True)
    caminho = os.path.join(pasta_destino, file.filename)
    file.save(caminho)
    return "Enviado com sucesso", 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

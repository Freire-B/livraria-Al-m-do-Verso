import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dao import LivroDAO, MensagemDAO
from models import MensagemContato

app = Flask(__name__)
CORS(app)

# Diretório para armazenamento dos arquivos de imagem enviados
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

livro_dao = LivroDAO()
mensagem_dao = MensagemDAO()

@app.route("/api/livros", methods=["GET"])
def listar_livros():
    termo = request.args.get("busca", "")
    limite = int(request.args.get("limite", 4))
    offset = int(request.args.get("offset", 0))
    livros = livro_dao.buscar_todos(termo, limite, offset)
    return jsonify([l.to_dict() for l in livros]), 200

@app.route("/api/livros/<int:id_livro>", methods=["GET"])
def detalhe_livro(id_livro):
    livro = livro_dao.buscar_por_id(id_livro)
    if livro:
        return jsonify(livro.to_dict()), 200
    return jsonify({"erro": "Livro não encontrado"}), 404

# Endpoint para receber o arquivo de imagem via formulário (POST Multipart)
@app.route("/api/upload", methods=["POST"])
def upload_imagem():
    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhum arquivo de imagem enviado"}), 400

    file = request.files["imagem"]
    if file.filename == "":
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400

    filename = secure_filename(file.filename)
    caminho_salvar = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(caminho_salvar)

    url_imagem = f"http://127.0.0.1:5000/uploads/{filename}"
    return jsonify({"mensagem": "Imagem enviada com sucesso!", "url": url_imagem}), 201

# Endpoint para servir as imagens enviadas
@app.route("/uploads/<filename>", methods=["GET"])
def carregar_imagem(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/api/contato", methods=["POST"])
def salvar_mensagem():
    dados = request.json
    if not dados or not dados.get("nome") or not dados.get("email") or not dados.get("mensagem"):
        return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

    nova_msg = MensagemContato(
        id_mensagem=None,
        nome=dados["nome"],
        email=dados["email"],
        data_atendimento=dados.get("data"),
        mensagem=dados["mensagem"]
    )
    id_gerado = mensagem_dao.inserir(nova_msg)
    return jsonify({"id": id_gerado, "mensagem": "Enviado com sucesso!"}), 201

@app.route("/api/mensagens", methods=["GET"])
def listar_mensagens():
    mensagens = mensagem_dao.buscar_todas()
    return jsonify([m.to_dict() for m in mensagens]), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
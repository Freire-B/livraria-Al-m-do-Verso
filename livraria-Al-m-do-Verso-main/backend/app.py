import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dao import LivroDAO, MensagemDAO
from models import MensagemContato

app = Flask(__name__)
CORS(app)

# Configuração da pasta de uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

livro_dao = LivroDAO()
mensagem_dao = MensagemDAO()


def salvar_imagem_upload(arquivo):
    """Salva o arquivo enviado na pasta uploads e retorna a URL local."""
    nome_seguro = secure_filename(arquivo.filename)
    caminho_destino = os.path.join(app.config["UPLOAD_FOLDER"], nome_seguro)
    arquivo.save(caminho_destino)
    return f"http://127.0.0.1:5000/uploads/{nome_seguro}"

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


@app.route("/api/livros", methods=["POST"])
def cadastrar_livro():
    titulo = request.form.get("titulo", "").strip()
    autor = request.form.get("autor", "").strip()
    preco = request.form.get("preco", "").strip()
    sinopse = request.form.get("sinopse", "").strip()
    id_categoria = request.form.get("id_categoria", "").strip()
    imagem_url = request.form.get("imagem_url", "").strip()

    if not all([titulo, autor, preco, id_categoria]):
        return jsonify({"erro": "Preencha título, autor, preço e categoria."}), 400

    arquivo = request.files.get("imagem")
    if arquivo and arquivo.filename:
        imagem_url = salvar_imagem_upload(arquivo)

    if not imagem_url:
        return jsonify({"erro": "Envie uma capa do dispositivo ou informe uma URL."}), 400

    try:
        novo_id = livro_dao.inserir(
            titulo=titulo,
            autor=autor,
            preco=float(preco.replace(",", ".")),
            imagem=imagem_url,
            sinopse=sinopse,
            id_categoria=int(id_categoria)
        )
        return jsonify({"mensagem": "Livro cadastrado com sucesso!", "id_livro": novo_id}), 201
    except ValueError:
        return jsonify({"erro": "Preço ou categoria inválidos."}), 400

@app.route("/api/upload", methods=["POST"])
def upload_imagem():
    arquivo = request.files.get("imagem")
    if not arquivo or not arquivo.filename:
        return jsonify({"erro": "Nenhum arquivo enviado."}), 400

    url_gerada = salvar_imagem_upload(arquivo)
    return jsonify({"url": url_gerada}), 201


@app.route("/uploads/<path:nome_arquivo>", methods=["GET"])
def servir_upload(nome_arquivo):
    return send_from_directory(app.config["UPLOAD_FOLDER"], nome_arquivo)

@app.route("/api/contato", methods=["POST"])
def enviar_contato():
    dados = request.get_json() or request.form
    nova_mensagem = MensagemContato(
        nome=dados.get("nome"),
        email=dados.get("email"),
        data_atendimento=dados.get("data_atendimento"),
        mensagem=dados.get("mensagem")
    )
    mensagem_dao.salvar(nova_mensagem)
    return jsonify({"mensagem": "Mensagem enviada com sucesso!"}), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
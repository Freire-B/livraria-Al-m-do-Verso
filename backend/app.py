from flask import Flask, request, jsonify
from flask_cors import CORS
from dao import LivroDAO, MensagemDAO
from models import MensagemContato

app = Flask(__name__)
CORS(app)  # Libera requisições de outras origens (Front-end DWS)

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
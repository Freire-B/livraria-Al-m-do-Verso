import sqlite3
from models import Livro, MensagemContato

class LivroDAO:
    def __init__(self, caminho_banco="livrera.db"):
        self.caminho_banco = caminho_banco

    def buscar_todos(self, termo="", limite=10, offset=0):
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()
            query = """
                SELECT id_livro, titulo, autor, preco, imagem, sinopse, id_categoria 
                FROM livros 
                WHERE titulo LIKE ? 
                ORDER BY id_livro ASC 
                LIMIT ? OFFSET ?
            """
            cursor.execute(query, (f"%{termo}%", limite, offset))
            linhas = cursor.fetchall()
            return [Livro(*linha) for linha in linhas]

    def buscar_por_id(self, id_livro):
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT id_livro, titulo, autor, preco, imagem, sinopse, id_categoria 
                FROM livros WHERE id_livro = ?
            """, (id_livro,))
            linha = cursor.fetchone()
            return Livro(*linha) if linha else None

class MensagemDAO:
    def __init__(self, caminho_banco="livrera.db"):
        self.caminho_banco = caminho_banco

    def inserir(self, mensagem_obj):
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO mensagens (nome, email, data_atendimento, mensagem) 
                VALUES (?, ?, ?, ?)
            """, (mensagem_obj.nome, mensagem_obj.email, mensagem_obj.data_atendimento, mensagem_obj.mensagem))
            conexao.commit()
            return cursor.lastrowid

    def buscar_todas(self):
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT id_mensagem, nome, email, data_atendimento, mensagem, data_envio 
                FROM mensagens ORDER BY data_envio DESC
            """)
            linhas = cursor.fetchall()
            return [MensagemContato(*linha) for linha in linhas]
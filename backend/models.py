class Livro:
    def __init__(self, id_livro, titulo, autor, preco, imagem, sinopse, id_categoria):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.preco = preco
        self.imagem = imagem
        self.sinopse = sinopse
        self.id_categoria = id_categoria

    def to_dict(self):
        return {
            "id_livro": self.id_livro,
            "titulo": self.titulo,
            "autor": self.autor,
            "preco": self.preco,
            "imagem": self.imagem,
            "sinopse": self.sinopse,
            "id_categoria": self.id_categoria
        }

class MensagemContato:
    def __init__(self, id_mensagem, nome, email, data_atendimento, mensagem, data_envio=None):
        self.id_mensagem = id_mensagem
        self.nome = nome
        self.email = email
        self.data_atendimento = data_atendimento
        self.mensagem = mensagem
        self.data_envio = data_envio

    def to_dict(self):
        return {
            "id_mensagem": self.id_mensagem,
            "nome": self.nome,
            "email": self.email,
            "data_atendimento": self.data_atendimento,
            "mensagem": self.mensagem,
            "data_envio": self.data_envio
        }
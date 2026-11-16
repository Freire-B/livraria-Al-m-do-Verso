CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    cidade TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS livros (
    id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    preco REAL NOT NULL,
    imagem TEXT NOT NULL,
    sinopse TEXT,
    id_categoria INTEGER NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    data_pedido TEXT NOT NULL,
    status TEXT NOT NULL,
    valor_total REAL NOT NULL,
    id_cliente INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,
    id_livro INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_livro) REFERENCES livros(id_livro)
);

CREATE TABLE IF NOT EXISTS mensagens (
    id_mensagem INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    data_atendimento TEXT,
    mensagem TEXT NOT NULL,
    data_envio DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO categorias (id_categoria, nome) VALUES 
(1, 'Mangás'), 
(2, 'HQs'), 
(3, 'Romance');

INSERT INTO clientes (id_cliente, nome, email, cidade) VALUES 
(1, 'Ana Souza', 'ana@email.com', 'Campinas'),
(2, 'Bruno Lima', 'bruno@email.com', 'Hortolândia'),
(3, 'Carla Mendes', 'carla@email.com', 'Sumaré');

INSERT INTO livros (id_livro, titulo, autor, preco, imagem, sinopse, id_categoria) VALUES 
(1, 'Diário de uma Apotecária Vol. 1', 'Natsu Hyuuga', 45.90, 'https://cdn.myanimelist.net/images/manga/3/201270.jpg', 'Maomao trabalhava como apotecária no bairro da luz...', 1),
(2, 'Lampião Vol. 1', 'Amatsu Carlo', 39.90, 'https://m.media-amazon.com/images/I/619QYdbHjWL._AC_UF1000,1000_QL80_.jpg', 'Uma releitura no cangaço nordestino...', 2),
(3, 'Demon Slayer Vol. 1', 'Koyoharu Gotouge', 34.90, 'https://cdn.myanimelist.net/images/manga/3/179023.jpg', 'Tanjiro parte em jornada para salvar sua irmã...', 1),
(4, 'Jujutsu Kaisen Vol. 1', 'Gege Akutami', 49.90, 'https://cdn.myanimelist.net/images/manga/3/210341.jpg', 'Yuuji Itadori se inscreve no Clube de Ocultismo...', 1);

INSERT INTO pedidos (id_pedido, data_pedido, status, valor_total, id_cliente) VALUES 
(101, '2026-11-01', 'entregue', 49.90, 1),
(102, '2026-11-03', 'pendente', 85.80, 2);

SELECT l.titulo, l.preco, c.nome AS categoria 
FROM livros l 
INNER JOIN categorias c ON l.id_categoria = c.id_categoria;

SELECT c.nome, c.email 
FROM clientes c 
LEFT JOIN pedidos p ON c.id_cliente = p.id_cliente 
WHERE p.id_pedido IS NULL;

SELECT titulo, preco FROM livros 
WHERE preco > (SELECT AVG(preco) FROM livros);

SELECT id_livro, titulo, preco FROM livros 
ORDER BY titulo ASC, id_livro ASC 
LIMIT 2 OFFSET 0;
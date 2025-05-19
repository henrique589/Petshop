import sqlite3
import hashlib

def gerar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_tabelas():
    conn =  sqlite3.connect('petshop.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            telefone TEXT,
            cpf TEXT NOT NULL UNIQUE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER UNIQUE,
            cargo TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL       
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
    ''')

    cursor.execute('DROP TABLE IF EXISTS pets')

    cursor.execute('''
        CREATE TABLE pets (
            id_pet INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            id_dono INTEGER NOT NULL,
            raca TEXT NOT NULL,
            idade INTEGER NOT NULL,
            peso INTEGER NOT NULL,
            tipo_animal TEXT NOT NULL,
            FOREIGN KEY (id_dono) REFERENCES clientes(id)
        )
    ''')

    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (id, nome, email, senha, tipo)
        VALUES (1, 'Administrador', 'admin@petshop.com', ?, 'gerente')
    ''', (gerar_senha('admin123'),))

    conn.commit()
    conn.close()
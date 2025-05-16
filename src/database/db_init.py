import sqlite3
import hashlib

def gerar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_tabelas():
    conn =  sqlite3.connect('petshop.db')
    cursor = conn.cursor()
    # Tabela usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    ''')

    # Tabela clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            telefone TEXT,
            cpf TEXT NOT NULL UNIQUE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    # Tabela funcionarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER UNIQUE,
            cargo TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    # Tabela produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL       
        )
    ''')

    # Tabela servicos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
    ''')

    # Tabela pets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            id_pet INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nome_dono TEXT NOT NULL,
            raca TEXT NOT NULL,
            idade INTEGER NOT NULL,
            peso INTEGER NOT NULL,
            tipo_animal TEXT NOT NULL
        )
    ''')

   # cursor.execute("DELETE FROM usuarios WHERE email = 'elder@gmail.com'")

    # Cadastro gerente
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (id, nome, email, senha, tipo)
        VALUES (1, 'Administrador', 'admin@petshop.com', ?, 'gerente')
    ''', (gerar_senha('admin123'),))

    conn.commit()
    conn.close()
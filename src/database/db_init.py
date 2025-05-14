import sqlite3
import hashlib

def gerar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_tabelas():
    conn =  sqlite3.connect('petshop.db')
    cursor = conn.cursor()
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
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    ''')

    # Cadastro gerente
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (id, nome, email, senha, tipo)
        VALUES (1, 'Administrador', 'admin@petshop.com', ?, 'gerente')
    ''', (gerar_senha('admin123'),))

    conn.commit()
    conn.close()
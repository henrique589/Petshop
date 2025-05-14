import sqlite3

def criar_tabelas():
    conn =  sqlite3.connect('petshop.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE
        )
                   
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL       
        )
                   
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
                   
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
    conn.commit()
    conn.close()
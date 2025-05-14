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
<<<<<<< HEAD
        )          
=======
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
<<<<<<< HEAD
>>>>>>> f5b04a52cc22797c11d08fe1aa0a13a30d815be6
=======
>>>>>>> f5b04a52cc22797c11d08fe1aa0a13a30d815be6
    ''')
    conn.commit()
    conn.close()
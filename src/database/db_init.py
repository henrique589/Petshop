import sqlite3
import hashlib
import os

def gerar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_tabelas():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, '..', '..', 'petshop.db')
    conn = sqlite3.connect(db_path)
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            id_pet INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            id_dono INTEGER NOT NULL,
            raca TEXT NOT NULL,
            idade INTEGER NOT NULL,
            peso REAL NOT NULL,
            tipo_animal TEXT NOT NULL,
            FOREIGN KEY (id_dono) REFERENCES clientes(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            pet_id INTEGER NOT NULL,
            servico_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (pet_id) REFERENCES pets(id_pet),
            FOREIGN KEY (servico_id) REFERENCES servicos(id)
        );
    ''')

    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (id, nome, email, senha, tipo)
        VALUES (1, 'Administrador', 'admin@petshop.com', ?, 'gerente')
    ''', (gerar_senha('admin123'),))

    conn.commit()
    conn.close()

# Executar diretamente se rodar o script
if __name__ == '__main__':
    criar_tabelas()

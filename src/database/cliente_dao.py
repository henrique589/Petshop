import sqlite3
from model.cliente import Cliente

class ClienteDAO:
    def __init__(self, db_path='petshop.db'):
        self.db_path = db_path

    def salvar(self, cliente: Cliente):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, email, telefone, cpf)
            VALUES (?, ?, ?, ?)
        ''', (cliente.nome, cliente.email, cliente.telefone, cliente.cpf))
        conn.commit()
        conn.close()
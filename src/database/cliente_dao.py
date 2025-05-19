import sqlite3
import os
from model.cliente import Cliente

class ClienteDAO:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', '..', 'petshop.db')

    def salvar(self, cliente: Cliente):
        print("Usando banco:", self.db_path)  
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO clientes (usuario_id, telefone, cpf)
            VALUES (?, ?, ?)
        ''', (cliente.usuario_id, cliente.telefone, cliente.cpf))

        conn.commit()
        conn.close()

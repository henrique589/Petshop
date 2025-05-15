import sqlite3
from model.funcionario import Funcionario

class FuncionarioDAO:
    def __init__(self, db_path='petshop.db'):
        self.db_path = db_path

    def salvar(self, funcionario: Funcionario):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO funcionarios (usuario_id, cargo)
            VALUES (?, ?)
        ''', (funcionario.usuario_id, funcionario.cargo))
        conn.commit()
        conn.close()
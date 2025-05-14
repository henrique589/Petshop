import sqlite3
from model.servico import Servico

class ServicoDAO:
    def __init__(self, db_path='petshop.db'):
        self.db_path = db_path
    
    def adicionar(self, servico: Servico):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO servicos (nome, descricao, preco, estoque)
            VALUES (?, ?, ?, ?)
        ''', (servico.nome, servico.descricao, servico.preco, servico.estoque))
        conn.commit()
        conn.close()
    
    def atualizar(self, servico: Servico):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE servicos SET nome=?, descricao=?, preco=?, estoque=?
            WHERE id=?
        ''', (servico.nome, servico.descricao, servico.preco, servico.estoque, servico.id))
        conn.commit()
        conn.close()

    def remover(self, servico: Servico):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM servicos WHERE id=?", (servico.id,))
        conn.commit()
        conn.close()
    
    def listar(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servicos")
        linhas = cursor.fetchall()
        return [Servico[*linha] for linha in linhas]
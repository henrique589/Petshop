import sqlite3
from model.produto import Produto
import os

class ProdutoDAO:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', '..', 'petshop.db')
    
    def adicionar(self, produto: Produto):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, preco, estoque)
            VALUES (?, ?, ?, ?)
        ''', (produto.nome, produto.descricao, produto.preco, produto.estoque))
        conn.commit()
        conn.close()
    
    def atualizar(self, produto: Produto):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE produtos SET nome=?, descricao=?, preco=?, estoque=?
            WHERE id=?
        ''', (produto.nome, produto.descricao, produto.preco, produto.estoque, produto.id))
        conn.commit()
        conn.close()

    def remover(self, produto_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id=?", (produto_id,))
        conn.commit()
        conn.close()
    
    def listar(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, descricao, preco, estoque FROM produtos")
        linhas = cursor.fetchall()
        produtos = []
        for linha in linhas:
            id, nome, descricao, preco, estoque = linha
            produtos.append(Produto(id, nome, descricao, preco, estoque))
        conn.close()
        return produtos

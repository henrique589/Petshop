from model.produto import Produto
from database.produto_dao import ProdutoDAO
from view.produto_view import (
    obter_dados_produto,
    obter_id_produto,
    mostrar_produtos
) 

class ProdutoController:
    def __init__(self):
        self.dao = ProdutoDAO()

    def cadastrar_produto(self):
        nome, descricao, preco, estoque = obter_dados_produto()
        produto = Produto(None, nome, descricao, preco, estoque)
        self.dao.adicionar(produto)

    def atualizar_produto(self):
        id_produto = obter_id_produto()
        nome, descricao, preco, estoque = obter_dados_produto()
        produto = Produto(id_produto, nome, descricao, preco, estoque)
        self.dao.atualizar(produto)

    def remover_produto(self):
        id_produto = obter_id_produto()
        self.dao.remover(id_produto)

    def listar_produtos(self):
        produtos = self.dao.listar()
        mostrar_produtos(produtos)
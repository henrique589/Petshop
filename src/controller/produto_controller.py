from model.produto import Produto
from database.produto_dao import ProdutoDAO

class ProdutoController:
    def __init__(self):
        self.dao = ProdutoDAO()

    def cadastrar_produto(self, nome, descricao, preco, estoque):
        produto = Produto(nome=nome, descricao=descricao, preco=preco, estoque=estoque)
        self.dao.adicionar(produto)

    def atualizar_produto(self, id, nome, descricao, preco, estoque):
        produto = Produto(id=id, nome=nome, descricao=descricao, preco=preco, estoque=estoque)
        self.dao.atualizar(produto)

    def remover_produto(self, id):
        self.dao.remover(id)

    def listar_produtos(self):
        return self.dao.listar()
from model.servico import Servico
from database.servico_dao import ServicoDAO

class ServicoController:
    def __init__(self):
        self.dao = ServicoDAO()

    def cadastrar_servico(self, nome, descricao, preco, estoque):
        servico = Servico(nome=nome, descricao=descricao, preco=preco, estoque=estoque)
        self.dao.adicionar(servico)

    def atualizar_servico(self, id, nome, descricao, preco, estoque):
        servico = Servico(id=id, nome=nome, descricao=descricao, preco=preco, estoque=estoque)
        self.dao.atualizar(servico)

    def remover_servico(self, id):
        self.dao.remover(id)

    def listar_servicos(self):
        return self.dao.listar()
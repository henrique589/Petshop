from model.servico import Servico
from database.servico_dao import ServicoDAO
from view.servico_view import (
    obter_dados_servico,
    obter_id_servico,
    mostrar_servicos
)

class ServicoController:
    def __init__(self):
        self.dao = ServicoDAO()

    def cadastrar_servico(self):
        nome, descricao, preco, estoque = obter_dados_servico()
        servico = Servico(nome=nome, descricao=descricao, preco=preco, estoque=estoque)
        self.dao.adicionar(servico)

    def atualizar_servico(self):
        id_servico = obter_id_servico()
        nome, descricao, preco, estoque = obter_dados_servico()
        servico = Servico(id_servico, nome, descricao, preco, estoque)
        self.dao.atualizar(servico)

    def remover_servico(self):
        id_servico = obter_id_servico()
        self.dao.remover(id_servico)

    def listar_servicos(self):
        servicos = self.dao.listar()
        mostrar_servicos(servicos)
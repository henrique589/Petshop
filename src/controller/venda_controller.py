from model.venda import Venda
from database.venda_dao import VendaDAO
from database.usuario_dao import UsuarioDAO 
from datetime import datetime

class VendaController:
    def __init__(self):
        self.venda_dao = VendaDAO()
        self.usuario_dao = UsuarioDAO()

    def processar_venda(self, email_funcionario, itens_carrinho, cliente_id=None):
        id_funcionario = self.usuario_dao.get_funcionario_id_por_email(email_funcionario)

        if not id_funcionario:
            print(f"ERRO: Funcionário com email {email_funcionario} não encontrado.")
            return None

        valor_total = sum(item['preco'] * item['quantidade'] for item in itens_carrinho)

        nova_venda = Venda(
            cliente_id=cliente_id,
            funcionario_id=id_funcionario,
            valor_total=valor_total,
            data_venda=datetime.now()
        )
        nova_venda.itens = itens_carrinho 

        venda_id = self.venda_dao.registrar_venda(nova_venda)

        return venda_id
    
    def listar_todas_vendas(self):
        vendas = self.venda_dao.listar_todas_vendas()
        return [
            {"id": v[0], "data": v[1], "total": v[2], "cliente": v[3]} for v in vendas
        ]

    def compra_por_cliente(self, cliente_id, itens_carrinho):
        valor_total = sum(item['preco'] * item['quantidade'] for item in itens_carrinho)

        nova_venda = Venda(
            cliente_id=cliente_id,
            funcionario_id=None,  
            valor_total=valor_total,
            data_venda=datetime.now()
        )
        nova_venda.itens = itens_carrinho

        venda_id = self.venda_dao.registrar_venda(nova_venda)

        return venda_id

    def obter_historico_cliente(self, cliente_id):
        return self.venda_dao.listar_compras_por_cliente(cliente_id)
    
    def obter_detalhes_recibo(self, venda_id):
        return self.venda_dao.get_detalhes_venda_por_id(venda_id)

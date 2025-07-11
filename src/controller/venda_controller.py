from model.venda import Venda
from database.venda_dao import VendaDAO
from database.usuario_dao import UsuarioDAO 

class VendaController:
    def __init__(self):
        self.venda_dao = VendaDAO()

    def processar_venda(self, email_funcionario, itens_carrinho, cliente_id=None):
        id_funcionario = 1 

        valor_total = sum(item['preco'] * item['quantidade'] for item in itens_carrinho)

        nova_venda = Venda(
            cliente_id=cliente_id,
            funcionario_id=id_funcionario,
            valor_total=valor_total
        )
        nova_venda.itens = itens_carrinho 

        venda_id = self.venda_dao.registrar_venda(nova_venda)

        return venda_id
    
    def listar_todas_vendas(self):
        vendas = self.venda_dao.listar_todas_vendas()
        return [
            {"id": v[0], "data": v[1], "total": v[2], "cliente": v[3]} for v in vendas
        ]


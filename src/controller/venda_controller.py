from model.venda import Venda
from database.venda_dao import VendaDAO
from database.usuario_dao import UsuarioDAO # Precisaremos para pegar o ID do funcionário

class VendaController:
    def __init__(self):
        self.venda_dao = VendaDAO()
        # Este DAO será usado para buscar o ID do funcionário a partir do email na sessão
        # (Precisaremos adaptar o UsuarioDAO ou FuncionarioDAO para isso)

    def processar_venda(self, email_funcionario, itens_carrinho, cliente_id=None):
        # Lógica para buscar o ID do funcionário pelo email (a ser implementada)
        # Por enquanto, vamos usar um ID fixo para teste, ex: 1
        id_funcionario = 1 # Placeholder

        valor_total = sum(item['preco'] * item['quantidade'] for item in itens_carrinho)

        nova_venda = Venda(
            cliente_id=cliente_id,
            funcionario_id=id_funcionario,
            valor_total=valor_total
        )
        nova_venda.itens = itens_carrinho # Adiciona a lista de itens ao objeto Venda

        venda_id = self.venda_dao.registrar_venda(nova_venda)

        return venda_id
    
    def compra_por_cliente(self, cliente_id, itens_carrinho):
        valor_total = sum(item['preco'] * item['quantidade'] for item in itens_carrinho)

        nova_venda = Venda(
            cliente_id=cliente_id,
            funcionario_id=None,  
            valor_total=valor_total
        )
        nova_venda.itens = itens_carrinho

        venda_id = self.venda_dao.registrar_venda(nova_venda)

        return venda_id

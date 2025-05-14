from model.cliente import Cliente
from view.cliente_view import solicitar_dados_cliente
from database.cliente_dao import ClienteDAO

def cadastrar_cliente():
    nome, email, telefone, cpf = solicitar_dados_cliente()
    cliente = Cliente(nome, email, telefone, cpf)
    dao = ClienteDAO()
    dao.salvar(cliente)
    print(f'Cliente cadastrado com sucesso!')
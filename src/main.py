from database.db_init import criar_tabelas
from controller.usuario_controller import (
    cadastrar_cliente,
    login_usuario
)
from controller.funcionario_controller import cadastrar_funcionario
from controller.produto_controller import ProdutoController
from controller.servico_controller import ServicoController

def tela_cliente():
    print("\n Menu do Cliente (em desenvolvimento)")
    # Aqui você poderá futuramente: agendar banho/tosa, cadastrar pet, etc.

def tela_funcionario():
    print("\n Menu do Funcionário (em desenvolvimento)")
    # Aqui você poderá futuramente: registrar atendimento, concluir serviço, etc.

def tela_gerente():
    produtoController = ProdutoController()
    servicoController = ServicoController()
    while True:
        print("\n👨‍💼 Menu do Gerente")
        print("1 - Cadastrar Funcionário")
        print("2 - Cadastrar Produto")
        print("3 - Atualizar Produto")
        print("4 - Remover Produto")
        print("5 - Listar Produtos")
        print("6 - Cadastrar Serviço")
        print("7 - Atualizar Serviço")
        print("8 - Remover Serviço")
        print("9 - Listar Serviços")
        print("10 - Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_funcionario()
        elif opcao == "2":
            produtoController.cadastrar_produto()
        elif opcao == "3":
            produtoController.atualizar_produto()
        elif opcao == "4":
            produtoController.remover_produto()
        elif opcao == "5":
            produtoController.listar_produtos()
        elif opcao == "6":
            servicoController.cadastrar_servico()
        elif opcao == "7":
            servicoController.atualizar_servico()
        elif opcao == "8":
            servicoController.remover_servico()
        elif opcao == "9":
            servicoController.listar_servicos()
        elif opcao == "10":
            break
        else:
            print("❌ Opção inválida.")

def tela_inicial():
    criar_tabelas()
    while True:
        print("\n Sistema Pet Shop")
        print("1 - Login")
        print("2 - Cadastrar novo cliente")
        print("3 - Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            tipo = login_usuario()
            if tipo == "cliente":
                tela_cliente()
            elif tipo == "funcionario":
                tela_funcionario()
            elif tipo == "gerente":
                tela_gerente()
        elif opcao == "2":
            cadastrar_cliente()
        elif opcao == "3":
            print("👋 Encerrando o sistema.")
            break
        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    tela_inicial()

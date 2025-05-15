from database.db_init import criar_tabelas
from controller.usuario_controller import (
    cadastrar_cliente,
    login_usuario
)
from controller.funcionario_controller import cadastrar_funcionario

def tela_cliente():
    print("\n Menu do Cliente (em desenvolvimento)")
    # Aqui você poderá futuramente: agendar banho/tosa, cadastrar pet, etc.

def tela_funcionario():
    print("\n Menu do Funcionário (em desenvolvimento)")
    # Aqui você poderá futuramente: registrar atendimento, concluir serviço, etc.

def tela_gerente():
    while True:
        print("\n👨‍💼 Menu do Gerente")
        print("1 - Cadastrar Funcionário")
        print("2 - Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar_funcionario()
        elif opcao == "2":
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

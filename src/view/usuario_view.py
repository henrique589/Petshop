def solicitar_dados_usuario():
    print("\nCadastro de Usuário")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    return nome, email, senha

def solicitar_dados_funcionario():
    nome = input("Nome do funcionário: ")
    cargo = input("Cargo: ")
    email = input("Email: ")
    senha = input("Senha: ")
    return nome, cargo, email, senha

def solicitar_login():
    print("\nLogin")
    email = input("Email: ")
    senha = input("Senha: ")
    return email, senha

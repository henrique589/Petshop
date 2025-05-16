from model.usuario import Usuario
from model.funcionario import Funcionario
from database.usuario_dao import UsuarioDAO
from database.funcionario_dao import FuncionarioDAO
from view.usuario_view import solicitar_dados_usuario
from view.funcionario_view import solicitar_dados_funcionario

class FuncionarioController:
    def __init__(self):
        self.funcionarioDao = FuncionarioDAO()

    def cadastrar_funcionario(self):
        nome, email, senha = solicitar_dados_usuario()
        usuario = Usuario(nome, email, senha, tipo='funcionario')
        usuarioDao = UsuarioDAO()
        usuario_id = usuarioDao.cadastrar_usuario_retornaid(usuario)
        cargo = solicitar_dados_funcionario()
        funcionario = Funcionario(usuario_id, cargo)
        self.funcionarioDao.adicionar(funcionario)
        print(f'✅ Cadastro de funcionário realizado com sucesso!')

    def atualizar_funcionario(self):
        id_funcionario = int(input('ID do Funcionário: ')) #id da tabela de funcionarios
        usuario_id = self.funcionarioDao.obter_usuario_id_por_funcionario_id(id_funcionario)
        if not usuario_id:
            print("Funcionário não encontrado.")
        
        nome, email, senha = solicitar_dados_usuario()
        usuario = Usuario(nome, email, senha, 'funcionario')
        cargo = solicitar_dados_funcionario()
        funcionario = Funcionario(usuario_id, cargo)
        self.funcionarioDao.atualizar_funcionario(usuario, funcionario)
        print("✅ Funcionário atualizado com sucesso.")

    def remover_funcionario(self):
        funcionario_id = int(input("ID do funcionario a ser removido: ")) # id da tabela de funcionarios
        self.funcionarioDao.remover_funcionario(funcionario_id)

    def listar_funcionarios(self):
        funcionarios = self.funcionarioDao.listar_funcionarios()

        if not funcionarios:
            print("⚠️ Nenhum funcionário cadastrado.")
            return

        print("\n📋 Lista de Funcionários:")
        print("-" * 100)
        for f in funcionarios:
            id_func, nome, email, cargo = f
            print(f"ID: {id_func} | Nome: {nome} | Email: {email} | Cargo: {cargo}")
        print("-" * 50)

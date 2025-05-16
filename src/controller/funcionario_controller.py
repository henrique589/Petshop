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
        self.funcionarioDao.salvar(funcionario)
        print(f'✅ Cadastro de funcionário realizado com sucesso!') 
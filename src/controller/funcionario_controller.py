from model.usuario import Usuario
from model.funcionario import Funcionario
from database.usuario_dao import UsuarioDAO
from database.funcionario_dao import FuncionarioDAO
from view.usuario_view import solicitar_dados_usuario
from view.funcionario_view import solicitar_dados_funcionario

def cadastrar_funcionario():
    nome, email, senha = solicitar_dados_usuario()
    usuario = Usuario(nome, email, senha, tipo='funcionario')
    usuario_dao = UsuarioDAO()
    usuario_id = usuario_dao.cadastrar_usuario_retornaid(usuario)
    cargo = solicitar_dados_funcionario()
    funcionario = Funcionario(usuario_id, cargo)
    funcionario_dao = FuncionarioDAO()
    funcionario_dao.salvar(funcionario)
    print(f'✅ Cadastro de funcionário realizado com sucesso!') 
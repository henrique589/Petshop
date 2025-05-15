from model.usuario import Usuario
from model.cliente import Cliente
from database.usuario_dao import UsuarioDAO
from database.cliente_dao import ClienteDAO
from view.usuario_view import solicitar_dados_usuario, solicitar_login
from view.cliente_view import solicitar_dados_cliente

def cadastrar_cliente():
    nome, email, senha = solicitar_dados_usuario()
    usuario = Usuario(nome, email, senha, tipo='cliente')
    usuario_dao = UsuarioDAO()
    usuario_id = usuario_dao.cadastrar_usuario_retornaid(usuario)
    telefone, cpf = solicitar_dados_cliente()
    cliente = Cliente(usuario_id, telefone, cpf)
    clienteDao = ClienteDAO()
    clienteDao.salvar(cliente)
    print(f'✅ Cadastro realizado com sucesso!')   

def login_usuario():
    email, senha = solicitar_login()
    dao = UsuarioDAO()
    resultado = dao.autenticar_usuario(email, senha)
    if resultado:
        print(f'✅ Login realizado com sucesso.')
        return resultado['tipo']
    else:
        print(f'❌ Credenciais inválidas.')
        return None
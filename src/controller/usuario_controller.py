from model.usuario import Usuario
from model.cliente import Cliente
from database.usuario_dao import UsuarioDAO
from database.cliente_dao import ClienteDAO

class UsuarioController:
    def __init__(self):
        self.usuarioDao = UsuarioDAO()

    def cadastrar_cliente(self, nome, email, senha, telefone, cpf):
        usuario = Usuario(nome, email, senha, tipo='cliente')
        usuario_id = self.usuarioDao.cadastrar_usuario_retornaid(usuario)

        cliente = Cliente(usuario_id, telefone, cpf)
        clienteDao = ClienteDAO()
        clienteDao.salvar(cliente)

        print("✅ Cliente cadastrado com sucesso!")

    def login_usuario(self, email, senha):
        resultado = self.usuarioDao.autenticar_usuario(email, senha)
        if resultado:
            print('✅ Login realizado com sucesso.')
            return resultado['tipo']
        else:
            print('❌ Credenciais inválidas.')
            return None
    def listar_usuarios(self):
        return self.usuarioDao.listar_todos()

    def criar_usuario(self, nome, email, senha, tipo):
        usuario = Usuario(nome, email, senha, tipo)
        usuario_id = self.usuarioDao.cadastrar_usuario_retornaid(usuario)

        if tipo == 'cliente':
            from model.cliente import Cliente
            from database.cliente_dao import ClienteDAO
            cliente = Cliente(usuario_id, telefone="", cpf="")
            ClienteDAO().salvar(cliente)

        elif tipo == 'funcionario':
            from model.funcionario import Funcionario
            from database.funcionario_dao import FuncionarioDAO
            funcionario = Funcionario(usuario_id, cargo="Não informado")
            FuncionarioDAO().adicionar(funcionario)


    def editar_usuario(self, id, nome, email, senha, tipo):
        self.usuarioDao.editar(id, nome, email, senha, tipo)

    def excluir_usuario(self, id):
        self.usuarioDao.excluir(id)
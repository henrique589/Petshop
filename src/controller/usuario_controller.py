from model.usuario import Usuario
from model.cliente import Cliente
from database.usuario_dao import UsuarioDAO
from database.cliente_dao import ClienteDAO

class UsuarioController:
    def __init__(self):
        self.usuarioDao = UsuarioDAO()
        self.cliente_dao = ClienteDAO()

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

    def buscar_clientes_e_pets(self, termo):
        if not termo:
            return []
        
        dados = self.cliente_dao.buscar_por_nome_ou_cpf(termo)

        # Agrupar pets por cliente para uma estrutura de dados mais limpa
        clientes_agrupados = {}
        for item in dados:
            cpf = item['cpf_cliente']
            if cpf not in clientes_agrupados:
                clientes_agrupados[cpf] = {
                    "nome_cliente": item['nome_cliente'],
                    "contato_cliente": item['contato_cliente'],
                    "cpf_cliente": item['cpf_cliente'],
                    "pets": []
                }
            
            if item['nome_pet']: # Adiciona o pet apenas se ele existir
                clientes_agrupados[cpf]['pets'].append({
                    "nome_pet": item['nome_pet'],
                    "raca_pet": item['raca_pet'],
                    "idade_pet": item['idade_pet'],
                    "tipo_animal_pet": item['tipo_animal_pet']
                })
        
        return list(clientes_agrupados.values())
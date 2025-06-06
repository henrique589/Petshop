from flask import Flask, request, redirect, url_for, session, send_file
from sqlite3 import IntegrityError
from controller.usuario_controller import UsuarioController
from controller.pet_controller import PetController
from controller.servico_controller import ServicoController
from model.servico import Servico
from controller.produto_controller import ProdutoController
from model.produto import Produto
import os

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto'

usuario_controller = UsuarioController()
pet_controller = PetController()
servico_controller = ServicoController()
produto_controller = ProdutoController()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, 'static')


@app.route('/')
def index():
    if 'usuario' in session:
        if session['tipo'] == 'cliente':
            return redirect('/perfil')
        elif session['tipo'] == 'funcionario':
            return redirect('/painel-funcionario')
    return send_file(os.path.join(HTML_DIR, 'login.html'))


@app.route('/cadastro')
def cadastro_get():
    return send_file(os.path.join(HTML_DIR, 'cadastro.html'))


@app.route('/cadastro', methods=['POST'])
def cadastro_post():
    try:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        telefone = request.form['telefone']
        cpf = request.form['cpf']

        usuario_controller.cadastrar_cliente(nome, email, senha, telefone, cpf)
        return "Cliente cadastrado com sucesso! <a href='/'>Voltar para login</a>"
    except IntegrityError:
        return redirect("/cadastro?erro=email")


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    tipo = usuario_controller.login_usuario(email, senha)
    if tipo:
        session['usuario'] = email
        session['tipo'] = tipo

        if tipo == 'cliente':
            return redirect('/perfil')
        if tipo == 'funcionario':
            return redirect('/painel-funcionario')
        if tipo == 'gerente':
            return redirect('/painel-gerente')
    return "Usuário ou senha inválidos. <a href='/'>Tentar novamente</a>"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/cadastro-pet')
def cadastro_pet_get():
    return send_file(os.path.join(HTML_DIR, 'cadastro_pet.html'))


@app.route('/cadastro-pet', methods=['POST'])
def cadastro_pet_post():
    if 'usuario' not in session:
        return redirect('/')

    email_dono = session['usuario']
    nome = request.form['nome']
    raca = request.form['raca']
    idade = int(request.form['idade'])
    peso = float(request.form['peso'])
    tipo_animal = request.form['tipo_animal']

    pet_controller.cadastrar_pet_web(
        nome, email_dono, raca, idade, peso, tipo_animal)
    return '', 204


@app.route('/editar-pet', methods=['POST'])
def editar_pet():
    if 'usuario' not in session:
        return {"erro": "Nao autenticado"}, 401

    pet_id = request.form['id_pet']
    nome = request.form['nome']
    raca = request.form['raca']
    idade = int(request.form['idade'])
    peso = float(request.form['peso'])
    tipo_animal = request.form['tipo_animal']

    pet_controller.editar_pet_web(pet_id, nome, raca, idade, peso, tipo_animal)
    return '', 204


@app.route('/excluir-pet', methods=['POST'])
def excluir_pet():
    if 'usuario' not in session:
        return {"erro": "Nao autenticado"}, 401

    pet_id = request.form['id_pet']
    pet_controller.excluir_pet_web(pet_id)
    return '', 204


@app.route('/perfil')
def perfil_cliente():
    if 'usuario' not in session:
        return redirect('/')
    return send_file(os.path.join(HTML_DIR, 'perfil.html'))


@app.route('/api/pets')
def api_listar_pets():
    if 'usuario' not in session:
        return {"erro": "Não autenticado"}, 401

    email = session['usuario']
    pets = pet_controller.listar_pets_por_email(email)
    return pets


@app.route('/painel-gerente')
def painel_gerente():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return redirect('/')
    return send_file(os.path.join(HTML_DIR, 'painel_gerente.html'))


@app.route('/api/usuarios')
def api_listar_usuarios():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401
    return usuario_controller.listar_usuarios()


@app.route('/api/usuarios', methods=['POST'])
def api_criar_usuario():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401

    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    tipo = request.form['tipo']

    usuario_controller.criar_usuario(nome, email, senha, tipo)
    return '', 204


@app.route('/api/editar-usuario', methods=['POST'])
def api_editar_usuario():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401

    usuario_id = request.form['id']
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    tipo = request.form['tipo']

    usuario_controller.editar_usuario(usuario_id, nome, email, senha, tipo)
    return '', 204


@app.route('/api/excluir-usuario', methods=['POST'])
def api_excluir_usuario():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401

    usuario_id = request.form['id']
    usuario_controller.excluir_usuario(usuario_id)
    return '', 204


@app.route('/api/servicos')
def api_listar_servicos():
    # MODIFICAÇÃO: Permitir o cliente a listar os serviços também:
    if 'usuario' not in session or session.get('tipo') not in ['gerente', 'cliente']:
        return {"erro": "Não autorizado"}, 403

    return servico_controller.listar_servicos()


@app.route('/api/servicos', methods=['POST'])
def api_criar_servico():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401

    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = float(request.form['preco'])
    estoque = int(request.form['estoque'])

    servico_controller.dao.adicionar(
        Servico(nome=nome, descricao=descricao, preco=preco, estoque=estoque))
    return '', 204


@app.route('/api/editar-servico', methods=['POST'])
def api_editar_servico():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401

    id_servico = int(request.form['id'])
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = float(request.form['preco'])
    estoque = int(request.form['estoque'])

    servico_controller.dao.atualizar(Servico(
        id=id_servico, nome=nome, descricao=descricao, preco=preco, estoque=estoque))
    return '', 204


@app.route('/api/excluir-servico', methods=['POST'])
def api_excluir_servico():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401

    id_servico = int(request.form['id'])
    servico_controller.dao.remover(id_servico)
    return '', 204


@app.route('/painel-servicos')
def painel_servicos():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return redirect('/')
    return send_file(os.path.join(HTML_DIR, 'painel_servicos.html'))


@app.route('/painel-produtos')
def painel_produtos():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return redirect('/')
    return send_file(os.path.join(HTML_DIR, 'painel_produtos.html'))


@app.route('/api/produtos')
def api_listar_produtos():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401

    produtos = produto_controller.dao.listar()
    return [
        {
            "id": p.id,
            "nome": p.nome,
            "descricao": p.descricao,
            "preco": p.preco,
            "estoque": p.estoque
        }
        for p in produtos
    ]


@app.route('/api/produtos', methods=['POST'])
def api_criar_produto():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401

    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = float(request.form['preco'])
    estoque = int(request.form['estoque'])

    produto = Produto(nome=nome, descricao=descricao,
                      preco=preco, estoque=estoque)
    produto_controller.dao.adicionar(produto)
    return '', 204


@app.route('/api/editar-produto', methods=['POST'])
def api_editar_produto():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401

    id_produto = int(request.form['id'])
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = float(request.form['preco'])
    estoque = int(request.form['estoque'])

    produto = Produto(id=id_produto, nome=nome,
                      descricao=descricao, preco=preco, estoque=estoque)
    produto_controller.dao.atualizar(produto)
    return '', 204


@app.route('/api/excluir-produto', methods=['POST'])
def api_excluir_produto():
    if 'usuario' not in session or session['tipo'] != 'gerente':
        return {"erro": "Não autorizado"}, 401

    id_produto = int(request.form['id'])
    produto_controller.dao.remover(id_produto)
    return '', 204


@app.route('/servicos-cliente')
def servicos_cliente():
    if 'usuario' not in session or session.get('tipo') != 'cliente':
        return redirect('/')
    return send_file(os.path.join(HTML_DIR, 'servicos_cliente.html'))


if __name__ == '__main__':
    app.run(debug=True)

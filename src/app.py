from flask import Flask, request, redirect, url_for, session, send_file, jsonify
from sqlite3 import IntegrityError
from controller.usuario_controller import UsuarioController
from controller.pet_controller import PetController
from controller.servico_controller import ServicoController
from model.servico import Servico
from controller.produto_controller import ProdutoController
from model.produto import Produto
from controller.cliente_controller import ClienteController
from database.cliente_dao import ClienteDAO
from controller.venda_controller import VendaController
from database.venda_dao import VendaDAO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto'

usuario_controller = UsuarioController()
pet_controller = PetController()
servico_controller = ServicoController()
produto_controller = ProdutoController()
cliente_dao = ClienteDAO()
cliente_controller = ClienteController()
vendas_controller = VendaController()
venda_dao = VendaDAO()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, 'static')


def get_cliente_id():
    email = session.get('usuario')
    if not email:
        return None
    return cliente_dao.get_id_por_email(email)


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


@app.route('/painel-funcionario')
def painel_funcionario():
    if 'usuario' not in session or session.get('tipo') not in ['funcionario', 'gerente']:
        return redirect(url_for('index'))

    return send_file(os.path.join(HTML_DIR, 'painel_funcionario.html'))


@app.route('/api/buscar-clientes')
def api_buscar_clientes():
    if 'usuario' not in session or session.get('tipo') not in ['funcionario', 'gerente']:
        return {"erro": "Não autorizado"}, 403

    termo_busca = request.args.get('termo')
    if not termo_busca:
        return {"erro": "Termo de busca não fornecido"}, 400

    clientes = usuario_controller.buscar_clientes_e_pets(termo_busca)
    return clientes


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
    if 'usuario' not in session or session['tipo'] not in ['gerente', 'funcionario']:
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


@app.route('/api/agendamentos', methods=['POST'])
def api_agendar_servico():
    if 'usuario' not in session or session['tipo'] != 'cliente':
        return {"erro": "Não autorizado"}, 401

    cliente_id = get_cliente_id()
    if not cliente_id:
        return {"erro": "Cliente não encontrado"}, 404

    try:
        pet_id = int(request.form['pet_id'])
        servico_id = int(request.form['servico_id'])
        data = request.form['data']
        hora = request.form['hora']

        cliente_controller.agendar_servico_web(
            cliente_id, pet_id, servico_id, data, hora)
        return '', 204

    except ValueError as e:
        return {"erro": str(e)}, 400


@app.route('/api/excluir-agendamento', methods=['POST'])
def api_excluir_agendamento():
    if 'usuario' not in session or session['tipo'] not in ['cliente', 'atendente', 'gerente', 'funcionario']:
        return {"erro": "Não autorizado"}, 401

    agendamento_id = int(request.form['id'])
    cliente_controller.remover_agendamento(agendamento_id)
    return '', 204


@app.route('/servicos-cliente')
def servicos_cliente():
    if 'usuario' not in session or session.get('tipo') != 'cliente':
        return redirect('/')
    return send_file(os.path.join(HTML_DIR, 'servicos_cliente.html'))


@app.route('/api/agendamentos-todos')
def api_listar_agendamentos_todos():
    if 'usuario' not in session or session['tipo'] not in ['funcionario', 'gerente']:
        return {"erro": "Não autorizado"}, 403

    data = request.args.get('data')  # filtro opcional
    return cliente_controller.agendamentoDao.listar_todos_com_detalhes(data)


@app.route('/api/agendamentos/detalhes')
def api_agendamentos_detalhados():
    if 'usuario' not in session or session['tipo'] != 'funcionario':
        return {"erro": "Acesso não autorizado"}, 403

    data = request.args.get('data')
    agendamentos = cliente_controller.agendamentoDao.listar_todos_com_detalhes(
        data)
    return agendamentos


@app.route('/api/agendamentos-cliente')
def api_agendamentos_cliente():
    if 'usuario' not in session or session['tipo'] != 'cliente':
        return {"erro": "Não autorizado"}, 401

    cliente_id = get_cliente_id()
    return cliente_controller.agendamentoDao.listar_todos_com_detalhes_cliente(cliente_id)


@app.route('/painel-venda-produtos')
def painel_venda_produtos():
    if 'usuario' not in session or session.get('tipo') not in ['gerente', 'funcionario']:
        return redirect('/')
    return send_file(os.path.join(HTML_DIR, 'painel_venda_produtos.html'))


@app.route('/api/registrar-venda', methods=['POST'])
def api_registrar_venda():
    if 'usuario' not in session or session.get('tipo') not in ['gerente', 'funcionario']:
        return jsonify({"erro": "Não autorizado"}), 403

    dados = request.get_json()
    itens_carrinho = dados.get('itens')

    if not itens_carrinho:
        return jsonify({"erro": "Carrinho vazio"}), 400

    email_funcionario = session['usuario']

    venda_id = vendas_controller.processar_venda(
        email_funcionario, itens_carrinho)
    if venda_id:
        return jsonify({"mensagem": "Venda registrada com sucesso!", "venda_id": venda_id})
    else:
        return jsonify({"erro": "Não foi possível registrar a venda."}), 500

@app.route('/api/vendas/recentes')
def api_vendas_recentes():
    if 'usuario' not in session or session.get('tipo') not in ['gerente', 'funcionario']:
        return jsonify({"erro": "Não autorizado."}), 403
    
    vendas_dia = venda_dao.listar_vendas_dia()

    vendas = [
        {
            "id": venda[0],
            "data": venda[1],
            "total": venda[2],
            "cliente": venda[3] if venda[3] is not None else "Não informado"
        }
        for venda in vendas_dia
    ]
    return vendas

@app.route('/gerar-relatorio-faturamento')
def gerar_relatorio_faturamento():
    vendas = VendaController().listar_todas_vendas()
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    largura, altura = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, altura - 50, "Relatório de Faturamento - PetShop")

    y = altura - 100
    total_geral = 0

    pdf.setFont("Helvetica", 12)
    for venda in vendas:
        data = venda['data']
        cliente = venda['cliente']
        valor = venda['total']
        pdf.drawString(50, y, f"{data} - Cliente: {cliente or 'Não identificado'} - R$ {valor:.2f}")
        y -= 20
        total_geral += valor
        if y < 80:
            pdf.showPage()
            y = altura - 50

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y - 30, f"Total de Vendas: R$ {total_geral:.2f}")

    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="relatorio_faturamento.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)

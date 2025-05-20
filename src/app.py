from flask import Flask, request, redirect, url_for, session, send_file
from sqlite3 import IntegrityError
from controller.usuario_controller import UsuarioController
from controller.pet_controller import PetController
import os

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto'

usuario_controller = UsuarioController()
pet_controller = PetController()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, 'static')

# Página inicial (com redirecionamento inteligente)
@app.route('/')
def index():
    if 'usuario' in session:
        if session['tipo'] == 'cliente':
            return redirect('/perfil')
        elif session['tipo'] == 'funcionario':
            return redirect('/painel-funcionario')  # futuro
    return send_file(os.path.join(HTML_DIR, 'login.html'))

# Página de cadastro (GET)
@app.route('/cadastro')
def cadastro_get():
    return send_file(os.path.join(HTML_DIR, 'cadastro.html'))

# Cadastro de cliente (POST)
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

# Login
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
            return redirect('/painel-funcionario')  # futuro
        if tipo == 'gerente':
            return redirect('/painel-gerente') # futuro
        else:
            return "Tipo de usuário não reconhecido. <a href='/logout'>Sair</a>"
    else:
        return "Usuário ou senha inválidos. <a href='/'>Tentar novamente</a>"

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Cadastro de PET - GET
@app.route('/cadastro-pet')
def cadastro_pet_get():
    return send_file(os.path.join(HTML_DIR, 'cadastro_pet.html'))

# Cadastro de PET - POST
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

    pet_controller.cadastrar_pet_web(nome, email_dono, raca, idade, peso, tipo_animal)

    return "🐶 Pet cadastrado com sucesso! <a href='/cadastro-pet'>Cadastrar outro</a>"

# Perfil do cliente (HTML)
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

if __name__ == '__main__':
    app.run(debug=True)

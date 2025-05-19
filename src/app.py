from flask import Flask, request, redirect, url_for, session, send_file
from sqlite3 import IntegrityError
from controller.usuario_controller import UsuarioController
import os

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto' 

usuario_controller = UsuarioController()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, 'static')

@app.route('/')
def index():
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
        return f"Login realizado com sucesso! Tipo: {tipo} <a href='/logout'>Sair</a>"
    else:
        return "Usuário ou senha inválidos. <a href='/'>Tentar novamente</a>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
from model.cliente import Cliente
from database.cliente_dao import ClienteDAO
from controller.funcionario_controller import cadastrar_funcionario

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    cpf = request.form['cpf']
    
    cliente = Cliente(nome, email, telefone, cpf)
    dao = ClienteDAO()
    dao.salvar(cliente)
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

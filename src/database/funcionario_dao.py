import sqlite3
import hashlib
from model.funcionario import Funcionario
from model.usuario import Usuario

class FuncionarioDAO:
    def __init__(self, db_path='petshop.db'):
        self.db_path = db_path

    def gerar_senha_hash(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def obter_usuario_id_por_funcionario_id(self, funcionario_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT usuario_id FROM funcionarios WHERE id = ?', (funcionario_id,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return resultado[0]  # retorna o usuario_id
        else:
            return None

    def adicionar(self, funcionario: Funcionario):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO funcionarios (usuario_id, cargo)
            VALUES (?, ?)
        ''', (funcionario.usuario_id, funcionario.cargo))
        conn.commit()
        conn.close()
    
    def atualizar_funcionario(self, usuario: Usuario, funcionario: Funcionario):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE usuarios
            SET nome = ?, email = ?, senha = ?
            WHERE id = ?
        ''', (
            usuario.nome,
            usuario.email,
            self.gerar_senha_hash(usuario.senha),
            funcionario.usuario_id  # mesma chave
        ))

        cursor.execute('''
            UPDATE funcionarios
            SET cargo = ?
            WHERE usuario_id = ?
        ''', (
            funcionario.cargo,
            funcionario.usuario_id
        ))

        conn.commit()
        conn.close()

    def remover_funcionario(self, funcionario_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT usuario_id FROM funcionarios WHERE id = ?', (funcionario_id,))
        resultado = cursor.fetchone()

        if resultado is None:
            print("❌ Funcionário não encontrado.")
            conn.close()
            return

        usuario_id = resultado[0]
        cursor.execute('DELETE FROM funcionarios WHERE id = ?', (funcionario_id,))
        cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))

        conn.commit()
        conn.close()

        print("✅ Funcionário removido com sucesso.")
    
    def listar_funcionarios(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT f.id, u.nome, u.email, f.cargo
            FROM funcionarios f
            JOIN usuarios u ON f.usuario_id = u.id
        ''')

        funcionarios = cursor.fetchall()
        conn.close()

        return funcionarios 

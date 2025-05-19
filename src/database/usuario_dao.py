import sqlite3
import os
from model.usuario import Usuario

class UsuarioDAO:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', '..', 'petshop.db')

    def cadastrar_usuario_retornaid(self, usuario):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, tipo)
            VALUES (?, ?, ?, ?)
        ''', (usuario.nome, usuario.email, usuario.senha, usuario.tipo))

        conn.commit()
        usuario_id = cursor.lastrowid
        conn.close()

        return usuario_id

    def autenticar_usuario(self, email, senha):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT nome, tipo FROM usuarios WHERE email = ? AND senha = ?
        ''', (email, senha))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return {'nome': resultado[0], 'tipo': resultado[1]}
        else:
            return None

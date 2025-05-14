import sqlite3
from model.usuario import Usuario
import hashlib

class UsuarioDAO:
    def __init__(self, db_path='petshop.db'):
        self.db_path  = db_path

    def gerar_senha_hash(self, senha:str):
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def cadastrar_usuario_retornaid(self, usuario):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, tipo)
            VALUES (?, ?, ?, ?)
        ''', (usuario.nome, usuario.email, self.gerar_senha_hash(usuario.senha), usuario.tipo))
        usuario_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return usuario_id
    
    def cadastrar_usuario(self, usuario:Usuario):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Usuarios (nome, email, senha, tipo)
            VALUES (?, ?, ?, ?)
        ''', (usuario.nome, usuario.email, self.gerar_senha_hash(usuario.senha), usuario.tipo))
        conn.commit()
        conn.close()

    def autenticar_usuario(self, email, senha):
        senha_hash = self.gerar_senha_hash(senha)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nome, tipo FROM usuarios WHERE email = ? AND senha = ?
        ''', (email, senha_hash))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            nome, tipo = resultado
            return {"nome": nome, "tipo": tipo}
        else:
            return None
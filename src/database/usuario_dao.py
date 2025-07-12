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

    def listar_todos(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, email, tipo FROM usuarios')
        resultado = cursor.fetchall()
        conn.close()

        return [
            {"id": row[0], "nome": row[1], "email": row[2], "tipo": row[3]}
            for row in resultado
        ]

    def editar(self, id, nome, email, senha, tipo):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuarios SET nome=?, email=?, senha=?, tipo=? WHERE id=?
        ''', (nome, email, senha, tipo, id))
        conn.commit()
        conn.close()

    def excluir(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def get_funcionario_id_por_email(self, email):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT f.id FROM funcionarios f
                JOIN usuarios u ON f.usuario_id = u.id
                WHERE u.email = ?
            ''', (email,))
            resultado = cursor.fetchone()
            
            return resultado[0] if resultado else None

        except sqlite3.Error as e:
            print(f"Erro ao buscar ID do funcionário por email: {e}")
            return None
        finally:
            conn.close()
import sqlite3
import os
from model.cliente import Cliente

class ClienteDAO:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', '..', 'petshop.db')

    def salvar(self, cliente: Cliente):
        print("Usando banco:", self.db_path)  
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO clientes (usuario_id, telefone, cpf)
            VALUES (?, ?, ?)
        ''', (cliente.usuario_id, cliente.telefone, cliente.cpf))

        conn.commit()
        conn.close()

    def buscar_por_nome_ou_cpf(self, termo_busca):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = """
            SELECT
                u.nome AS nome_cliente,
                c.telefone AS contato_cliente,
                c.cpf AS cpf_cliente,
                p.nome AS nome_pet,
                p.raca AS raca_pet,
                p.idade AS idade_pet,
                p.tipo_animal AS tipo_animal_pet
            FROM usuarios u
            JOIN clientes c ON u.id = c.usuario_id
            LEFT JOIN pets p ON c.id = p.id_dono
            WHERE u.nome LIKE ? OR c.cpf = ?
            ORDER BY u.nome;
        """
        
        # O termo para o LIKE precisa dos caracteres '%' para funcionar como "contém"
        termo_like = f'%{termo_busca}%'
        
        cursor.execute(query, (termo_like, termo_busca))
        
        resultados = cursor.fetchall()
        conn.close()

        clientes_e_pets = []
        if resultados:
            colunas = [description[0] for description in cursor.description]
            for linha in resultados:
                clientes_e_pets.append(dict(zip(colunas, linha)))

        return clientes_e_pets
    
    def get_id_por_email(self, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.id
            FROM clientes c
            JOIN usuarios u ON c.usuario_id = u.id
            WHERE u.email = ?
        ''', (email,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None

import sqlite3
import os
from model.pet import Pet

class PetDAO:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', '..', 'petshop.db')

    def salvar(self, pet):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO pets (nome, id_dono, raca, idade, peso, tipo_animal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (pet.nome, pet.id_dono, pet.raca, pet.idade, pet.peso, pet.tipo_animal))

        conn.commit()
        conn.close()

    def consultar_email_dono(self, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.id FROM clientes c
            JOIN usuarios u ON u.id = c.usuario_id
            WHERE u.email = ?
        ''', (email,))

        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None

    def listar_pets_por_email(self, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT p.id_pet, p.nome, p.raca, p.idade, p.peso, p.tipo_animal
            FROM pets p
            JOIN clientes c ON c.id = p.id_dono
            JOIN usuarios u ON u.id = c.usuario_id
            WHERE u.email = ?
        ''', (email,))

        pets = cursor.fetchall()
        conn.close()

        return [
            {
                "id_pet": row[0],
                "nome": row[1],
                "raca": row[2],
                "idade": row[3],
                "peso": row[4],
                "tipo_animal": row[5]
            }
            for row in pets
        ]

    def editar_pet(self, id_pet, nome, raca, idade, peso, tipo_animal):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pets
            SET nome = ?, raca = ?, idade = ?, peso = ?, tipo_animal = ?
            WHERE id_pet = ?
        ''', (nome, raca, idade, peso, tipo_animal, id_pet))
        conn.commit()
        conn.close()

    def excluir_pet(self, id_pet):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pets WHERE id_pet = ?', (id_pet,))
        conn.commit()
        conn.close()

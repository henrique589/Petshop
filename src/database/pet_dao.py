import sqlite3
from model.pet import Pet

class PetDAO:
    def __init__(self, db_path='petshop.db'):
        self.db_path = db_path

    def salvar(self, pet: Pet):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pets (nome, id_dono, raca, idade, peso, tipo_animal)
            VALUES (?, ?, ?, ?)
        ''', (pet.nome,pet.id_dono, pet.raca, pet.idade, pet.tipo_animal))
        conn.commit()
        conn.close()
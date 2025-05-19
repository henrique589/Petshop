from model.pet import Pet 
from view.pet_view import solicitar_dados_pet
from database.pet_dao import PetDAO

class PetController:

    def __init__(self):
        self.petDao = PetDAO()

    def cadastrar_pet(self):
        nome, nome_dono, raca, idade, peso, tipo_animal= solicitar_dados_pet()
        id_dono = self.petDao.consultar_nome_dono(nome_dono)
    
        pet = Pet(nome, id_dono, raca, idade, peso, tipo_animal)
        self.petDao.salvar(pet)
        print(f'Pet cadastrado com sucesso!')
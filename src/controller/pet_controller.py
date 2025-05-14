from model.pet import Pet 
from view.pet_view import solicitar_dados_pet
from database.pet_dao import PetDAO

def cadastrar_cliente():

    nome, nome_dono, raca, idade, peso, tipo_animal= solicitar_dados_pet()
    pet= Pet(nome, nome_dono, raca, idade, peso, tipo_animal)
    dao= PetDAO()
    dao.salvar(pet)
    print(f'Pet cadastrado com sucesso!')
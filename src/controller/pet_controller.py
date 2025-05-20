from model.pet import Pet 
from database.pet_dao import PetDAO

class PetController:
    def __init__(self):
        self.petDao = PetDAO()

    def cadastrar_pet_web(self, nome, email_dono, raca, idade, peso, tipo_animal):
        id_dono = self.petDao.consultar_email_dono(email_dono)

        if not id_dono:
            print("❌ Dono não encontrado com esse e-mail!")
            return

        pet = Pet(nome, id_dono, raca, idade, peso, tipo_animal)
        self.petDao.salvar(pet)

        print("✅ Pet cadastrado com sucesso!")

    def listar_pets_por_email(self, email_dono): 
        return self.petDao.listar_pets_por_email(email_dono)

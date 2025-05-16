import sqlite3
from database.pet_dao import PetDAO

def solicitar_dados_pet():
    nome = input("Nome: ")
    nome_dono= input("Nome do dono: ")
    dao=PetDAO()
    resultado_consulta= dao.consultar_nome_dono(nome_dono)
    
    if resultado_consulta:
        id_dono = resultado_consulta
        raca = input("Raça: ")
        idade = input("Idade: ")
        peso = input("Peso: ")
        tipo_animal = input("Tipo do animal: ")
        return nome, id_dono, raca, idade, peso, tipo_animal
    
    else:
        print("O dono inserido não está cadastrado, realize o cadastro e tente novamente.")
        return None

import sqlite3

def solicitar_dados_pet():
    nome = input("Nome: ")
    nome_dono= input("Nome do dono: ")
    
    
    if resultado:

    raca = input("Raça: ")
    idade = input("Idade: ")
    peso = input("Peso: ")
    tipo_animal = input("Tipo do animal: ")
    return nome, nome_dono, raca, idade, peso, tipo_animal


def consultar_nome_dono(nome_dono):

    conn =  sqlite3.connect('petshop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pets WHERE nome = ?", (nome_dono,))
    resultado= cursor.fetchone()
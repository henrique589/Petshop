import sqlite3

def solicitar_dados_pet():
    nome = input("Nome: ")
    nome_dono= input("Nome do dono: ")
    resultado_consulta= consultar_nome_dono(nome_dono)
    
    if resultado_consulta:
        raca = input("Raça: ")
        idade = input("Idade: ")
        peso = input("Peso: ")
        tipo_animal = input("Tipo do animal: ")
        return nome, nome_dono, raca, idade, peso, tipo_animal
    
    else:
        print("O dono inserido não está cadastrado, realize o cadastro e tente novamente.")
        return None


def consultar_nome_dono(nome_dono):

    conn =  sqlite3.connect('petshop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pets WHERE nome = ?", (nome_dono,))
    resultado= cursor.fetchone()
    conn.close()
    return resultado
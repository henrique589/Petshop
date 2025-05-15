def obter_dados_servico():
    nome = input("Nome: ")
    descricao = input("Descricao: ")
    preco = float(input("Preco: "))
    estoque = int(input("Estoque: "))
    return nome, descricao, preco, estoque

def obter_id_servico():
    return int(input("ID do Servico: "))

def mostrar_servicos(produtos):
    print("\n--- Lista de Servicos ---")
    for p in produtos:
        print(f"ID: {p.id} | Nome: {p.nome} | Preço: R${p.preco:.2f} | Estoque: {p.estoque}")

def obter_dados_produto():
    nome = input("Nome: ")
    descricao = input("Descricao: ")
    preco = float(input("Preco: "))
    estoque = int(input("Estoque: "))
    return nome, descricao, preco, estoque

def obter_id_produto():
    return int(input("ID do Produto: "))

def mostrar_produtos(produtos):
    print("\n--- Lista de Produtos ---")
    for p in produtos:
        print(f"ID: {p.id} | Nome: {p.nome} | Preço: R${p.preco:.2f} | Estoque: {p.estoque}")

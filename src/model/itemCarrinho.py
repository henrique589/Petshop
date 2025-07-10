class ItemCarrinho:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def subtotal(self):
        return self.produto.preco * self.quantidade

class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, produto, quantidade):
        for item in self.itens:
            if item.produto.id == produto.id:
                item.quantidade += quantidade
                return
        self.itens.append(ItemCarrinho(produto, quantidade))

    def total(self):
        return sum(item.subtotal() for item in self.itens)

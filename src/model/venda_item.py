class VendaItem:
    def __init__(self, id=None, venda_id=None, produto_id=None, quantidade=0, preco_unitario=0.0):
        self.id = id
        self.venda_id = venda_id
        self.produto_id = produto_id
        self.quantidade = 0
        self.preco_unitario = preco_unitario
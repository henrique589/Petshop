class Servico:
    def __init__(self, id=None, nome="", descricao="", preco=0.0, estoque=0):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
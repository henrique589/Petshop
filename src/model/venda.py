class Venda:
    def __init__(self, id=None, cliente_id=None, funcionario_id=None, data_venda=None, valor_total=0.0):
        self.id = id
        self.cliente_id = cliente_id
        self.funcionario_id = funcionario_id
        self.data_venda = data_venda
        self.valor_total = valor_total
        self.itens = []
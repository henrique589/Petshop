class Agendamento:
    def __init__(self, id=None, cliente_id=None, servico_id=None, data="", hora=""):
        self.id = id
        self.cliente_id = cliente_id
        self.servico_id = servico_id
        self.data = data
        self.hora = hora
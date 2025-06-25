class Agendamento:
    def __init__(self, id=None, cliente_id=None, pet_id=None, servico_id=None, data="", hora=""):
        self.id = id
        self.cliente_id = cliente_id
        self.pet_id = pet_id
        self.servico_id = servico_id
        self.data = data
        self.hora = hora

    def to_dict(self):
    
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "pet_id": self.pet_id,
            "servico_id": self.servico_id,
            "data": self.data,
            "hora": self.hora
        }

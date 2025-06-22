from model.agendamento import Agendamento
from database.agendamento_dao import AgendamentoDAO

class ClienteController:
    def __init__(self):
        self.agendamentoDao = AgendamentoDAO()

    def agendar_servico(self, cliente_id):
        print("Agendar banho e tosa")
        servico_id = int(input("ID do serviço (ex: 1 para banho, 2 para tosa): "))
        data = input("Data (AAAA-MM-DD): ")
        hora = input("Hora (HH:MM): ")

        agendamento = Agendamento(cliente_id=cliente_id, servico_id=servico_id, data=data, hora=hora)
        self.agendamentoDao.agendar(agendamento)
        print("✅ Agendamento realizado com sucesso!")

    def listar_agendamentos(self, cliente_id):
        agendamentos = self.agendamentoDao.listar_por_cliente(cliente_id)
        if not agendamentos:
            print("Nenhum agendamento encontrado.")
            return
        for ag in agendamentos:
            print(f"ID: {ag.id} | Serviço: {ag.servico_id} | Data: {ag.data} | Hora: {ag.hora}")

def agendar_servico_web(self, cliente_id, servico_id, data, hora):
    agendamento = Agendamento(cliente_id=cliente_id, servico_id=servico_id, data=data, hora=hora)
    self.agendamentoDao.agendar(agendamento)

from model.agendamento import Agendamento
from database.agendamento_dao import AgendamentoDAO
from datetime import datetime, timedelta

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

    from datetime import datetime, timedelta

    def agendar_servico_web(self, cliente_id, pet_id, servico_id, data_str, hora_str):
        # Converter data e hora em datetime
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M').time()
        datetime_agendamento = datetime.combine(data, hora)

        agora = datetime.now()

        if datetime_agendamento < agora:
            raise ValueError("Não é possível agendar um serviço para uma data ou hora anteriores à atual.")

        hora_abertura = datetime.strptime('07:00', '%H:%M').time()
        hora_fechamento = datetime.strptime('18:00', '%H:%M').time()
        if hora < hora_abertura or hora > hora_fechamento:
            raise ValueError("Horários disponíveis apenas entre 07:00 e 18:00.")

        agendamentos_no_dia = self.agendamentoDao.listar_por_data(data_str)

        intervalo = timedelta(minutes=30)

        for ag in agendamentos_no_dia:
            ag_data = datetime.strptime(ag.data, '%Y-%m-%d').date()
            ag_hora = datetime.strptime(ag.hora, '%H:%M').time()
            ag_datetime = datetime.combine(ag_data, ag_hora)

            diff = abs(datetime_agendamento - ag_datetime)
            if diff < intervalo:
                raise ValueError(f"Já existe um agendamento próximo a {ag.hora}. Por favor, escolha outro horário.")

        agendamento = Agendamento(
            cliente_id=cliente_id,
            pet_id=pet_id,
            servico_id=servico_id,
            data=data_str,
            hora=hora_str
        )
        self.agendamentoDao.agendar(agendamento)

    def remover_agendamento(self, agendamento_id):
        self.agendamentoDao.remover(agendamento_id)


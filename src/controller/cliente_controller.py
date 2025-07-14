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

    def horarios_disponiveis(self, data_str, hora_str):
        
        data = datetime.strptime(data_str, '%Y-%m-%d').date()

        hora_abertura = datetime.strptime('07:00', '%H:%M').time()
        hora_fechamento = datetime.strptime('18:00', '%H:%M').time()
        fim_dia = datetime.combine(data, hora_fechamento)


        agendamentos_no_dia = self.agendamentoDao.listar_por_data(data_str)

        intervalo = timedelta(minutes=30)

        agendamentos_no_dia = self.agendamentoDao.listar_por_data(data_str)
        agendados = set(
            datetime.combine(datetime.strptime(ag.data, '%Y-%m-%d').date(), 
                             datetime.strptime(ag.hora, '%H:%M').time())
            for ag in agendamentos_no_dia
        )

        aux = datetime.combine(data, hora_abertura)
        disponivel = []

        while aux <= fim_dia:
            conflito = False
            for ag in agendados:
                if abs(aux - ag) < intervalo:
                    conflito = True
                    break

            if not conflito:
                disponivel.append(aux.strftime('%H:%M'))

            aux += intervalo

        return disponivel



    def agendar_servico_web(self, cliente_id, pet_id, servico_id, data_str, hora_str):
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M').time()
        datetime_agendamento = datetime.combine(data, hora)

        agora = datetime.now()

        if datetime_agendamento < agora:
            raise ValueError("Não é possível agendar um serviço para uma data ou hora anteriores à atual.")

        hora_abertura = datetime.strptime('07:00', '%H:%M').time()
        hora_fechamento = datetime.strptime('18:00', '%H:%M').time()
        hora_proximo_fechamento = datetime.strptime('17:30', '%H:%M').time()
        if hora < hora_abertura or hora > hora_fechamento:
            raise ValueError("Horários disponíveis apenas entre 07:00 e 18:00.")
        elif hora > hora_proximo_fechamento:
            raise ValueError("Horário próximo ao fechamento, tente um horário no próximo dia!")

        agendamentos_no_dia = self.agendamentoDao.listar_por_data(data_str)

        intervalo = timedelta(minutes=30)

        agendamentos_no_dia = self.agendamentoDao.listar_por_data(data_str)
        agendados = set(
            datetime.combine(datetime.strptime(ag.data, '%Y-%m-%d').date(), 
                             datetime.strptime(ag.hora, '%H:%M').time())
            for ag in agendamentos_no_dia
        )

        horario_tentado = datetime_agendamento + intervalo
        fim_dia = datetime.combine(data, hora_fechamento)
        horario_livre = None

        while horario_tentado <= fim_dia:
            if horario_tentado not in agendados:
                horario_livre = horario_tentado
                break
            horario_tentado += intervalo

        '''
        aux = datetime.combine(data, datetime.strptime('07:00', '%H:%M').time())
        disponivel = []

        while aux <= fim_dia:
            conflito = False
            for ag in agendados:
                if abs(aux - ag) < intervalo:
                    conflito = True
                    break

            if not conflito:
                disponivel.append(aux.strftime('%H:%M'))

            aux += intervalo
        '''

        if horario_livre is None:
            raise ValueError("Não há horários disponíveis neste dia. Por favor, escolha outro dia.")
        #elif horario_livre:

        disponivel= self.horarios_disponiveis(data_str, hora_str)

        for ag in agendamentos_no_dia:
            ag_data = datetime.strptime(ag.data, '%Y-%m-%d').date()
            ag_hora = datetime.strptime(ag.hora, '%H:%M').time()
            ag_datetime = datetime.combine(ag_data, ag_hora)

            diff = abs(datetime_agendamento - ag_datetime)

            if diff < intervalo:
                raise ValueError(f"Já existe um agendamento as {ag.hora}. Por favor, consulte os horários disponíveis.")

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

    def editar_agendamento_web(self, agendamento_id, pet_id, servico_id, data_str, hora_str):
        from datetime import datetime, timedelta

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
            if ag.id == agendamento_id:
                continue  
            ag_data = datetime.strptime(ag.data, '%Y-%m-%d').date()
            ag_hora = datetime.strptime(ag.hora, '%H:%M').time()
            ag_datetime = datetime.combine(ag_data, ag_hora)
            if abs(datetime_agendamento - ag_datetime) < intervalo:
                raise ValueError(f"Já existe um agendamento próximo a {ag.hora}. Por favor, escolha outro horário.")

        from model.agendamento import Agendamento
        agendamento = Agendamento(
            id=agendamento_id,
            pet_id=pet_id,
            servico_id=servico_id,
            data=data_str,
            hora=hora_str
        )
        self.agendamentoDao.atualizar_agendamento(agendamento)
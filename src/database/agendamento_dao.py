import sqlite3
import os
from model.agendamento import Agendamento

class AgendamentoDAO:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', '..', 'petshop.db')
    
    def agendar(self, agendamento: Agendamento):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO agendamentos (cliente_id, servico_id, data, hora)
            VALUES (?, ?, ?, ?)
        ''', (agendamento.cliente_id, agendamento.servico_id, agendamento.data, agendamento.hora))
        conn.commit()
        conn.close()

    def listar_por_cliente(self, cliente_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, cliente_id, servico_id, data, hora
            FROM agendamentos
            WHERE cliente_id = ?
        ''', (cliente_id,))
        rows = cursor.fetchall()
        agendamentos = []
        for row in rows:
            id, cliente_id, servico_id, data, hora = row
            agendamentos.append(Agendamento(id, cliente_id, servico_id, data, hora))
        conn.close()
        return agendamentos

    def remover(self, agendamento_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agendamentos WHERE id = ?", (agendamento_id,))
        conn.commit()
        conn.close()

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
            INSERT INTO agendamentos (cliente_id, pet_id, servico_id, data, hora)
            VALUES (?, ?, ?, ?, ?)
        ''', (agendamento.cliente_id, agendamento.pet_id, agendamento.servico_id, agendamento.data, agendamento.hora))
        conn.commit()
        conn.close()

    def listar_por_data(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT id, cliente_id, pet_id, servico_id, data, hora FROM agendamentos WHERE data = ?
                       ''', (data,))
        rows = cursor.fetchall()
        agendamentos = []
        for row in rows:
            ag = Agendamento(*row)
            agendamentos.append(ag)
        conn.close()
        return agendamentos

    
    def existe_agendamento_em(self, data, hora):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM agendamentos
            WHERE data = ? AND hora = ?
        ''', (data, hora))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0


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

    def listar_todos_com_detalhes(self, data=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = '''
            SELECT a.id, a.data, a.hora,
                p.nome AS nome_pet,
                u.nome AS nome_cliente,
                s.nome AS nome_servico
            FROM agendamentos a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN usuarios u ON u.id = c.usuario_id
            JOIN servicos s ON a.servico_id = s.id
            JOIN pets p ON p.id_pet = a.pet_id
            WHERE 1 = 1
        '''


        params = []
        if data:
            query += " AND a.data = ?"
            params.append(data)

        query += " ORDER BY a.data, a.hora"

        cursor.execute(query, params)
        agendamentos = cursor.fetchall()
        conn.close()

        return [
            {
                "id": row[0],
                "data": row[1],
                "hora": row[2],
                "nome_pet": row[3],
                "nome_cliente": row[4],
                "nome_servico": row[5]
            } for row in agendamentos
        ]


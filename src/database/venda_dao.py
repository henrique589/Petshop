import sqlite3
import os

class VendaDAO:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', '..', 'petshop.db')

    def registrar_venda(self, venda):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO vendas (cliente_id, funcionario_id, valor_total, data_venda)
                VALUES (?, ?, ?, ?)
            ''', (venda.cliente_id, venda.funcionario_id, venda.valor_total, venda.data_venda))

            venda_id = cursor.lastrowid

            for item in venda.itens:
                cursor.execute('''
                    INSERT INTO venda_itens (venda_id, produto_id, quantidade, preco_unitario)
                    VALUES (?, ?, ?, ?)
                ''', (venda_id, item['id'], item['quantidade'], item['preco']))

                cursor.execute('''
                    UPDATE produtos SET estoque = estoque - ? WHERE id = ?
                ''', (item['quantidade'], item['id']))

            conn.commit()
            return venda_id 

        except sqlite3.Error as e:
            print(f"Erro ao registrar a venda: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def listar_vendas_dia(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT v.id, 
                strftime('%Y-%m-%dT%H:%M:%S', v.data_venda) as data_venda_iso,
                v.valor_total, 
                u.nome
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN usuarios u ON c.usuario_id = u.id
            WHERE DATE(v.data_venda) = DATE('now', 'localtime')
            ORDER BY v.data_venda DESC
        ''')
        vendas = cursor.fetchall()
        conn.close()
        return vendas
    
    def listar_todas_vendas(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT v.id,
                strftime('%Y-%m-%d %H:%M', v.data_venda) as data_venda,
                v.valor_total,
                u.nome
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN usuarios u ON c.usuario_id = u.id
            ORDER BY v.data_venda DESC
        ''')
        vendas = cursor.fetchall()
        conn.close()
        return vendas

    def listar_compras_por_cliente(self, cliente_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT id, data_venda, valor_total
                FROM vendas
                WHERE cliente_id = ?
                ORDER BY data_venda DESC
            ''', (cliente_id,))
            vendas = cursor.fetchall()

            historico_completo = []
            for venda in vendas:
                venda_dict = dict(venda)

                cursor.execute('''
                    SELECT 
                        vi.quantidade, 
                        vi.preco_unitario, 
                        p.nome as produto_nome
                    FROM venda_itens vi
                    JOIN produtos p ON vi.produto_id = p.id
                    WHERE vi.venda_id = ?
                ''', (venda_dict['id'],))
                itens = cursor.fetchall()
                
                # Adiciona a lista de itens ao dicionário da venda
                venda_dict['itens'] = [dict(item) for item in itens]
                historico_completo.append(venda_dict)
            
            return historico_completo

        except sqlite3.Error as e:
            print(f"Erro ao listar compras do cliente: {e}")
            return None
        finally:
            conn.close()

    # Dentro da classe VendaDAO em venda_dao.py

    def get_detalhes_venda_por_id(self, venda_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            # Query principal para buscar dados da venda, cliente e funcionário
            cursor.execute('''
                SELECT
                    v.id,
                    v.data_venda,
                    v.valor_total,
                    uc.nome as cliente_nome,
                    uf.nome as funcionario_nome
                FROM vendas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                LEFT JOIN usuarios uc ON c.usuario_id = uc.id
                LEFT JOIN funcionarios f ON v.funcionario_id = f.id
                LEFT JOIN usuarios uf ON f.usuario_id = uf.id
                WHERE v.id = ?
            ''', (venda_id,))
            venda = cursor.fetchone()

            if not venda:
                return None

            venda_dict = dict(venda)

            # Query para buscar os itens da venda
            cursor.execute('''
                SELECT 
                    vi.quantidade, 
                    vi.preco_unitario, 
                    p.nome as produto_nome
                FROM venda_itens vi
                JOIN produtos p ON vi.produto_id = p.id
                WHERE vi.venda_id = ?
            ''', (venda_id,))
            itens = cursor.fetchall()
            
            venda_dict['itens'] = [dict(item) for item in itens]
            return venda_dict

        except sqlite3.Error as e:
            print(f"Erro ao buscar detalhes da venda: {e}")
            return None
        finally:
            conn.close()
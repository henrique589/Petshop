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
                INSERT INTO vendas (cliente_id, funcionario_id, valor_total)
                VALUES (?, ?, ?)
            ''', (venda.cliente_id, venda.funcionario_id, venda.valor_total))

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
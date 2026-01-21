from database.db_manager import db
from core.logger import log_erro, log_info

class FinanceModel:
    
    @staticmethod
    def adicionar_despesa(descricao, categoria, valor, data, obs):
        # CORREÇÃO 1: Nome da coluna corrigido (era descicaom)
        query = """
        INSERT INTO despesas (descricao, categoria, valor, data_despesa, observacao)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            if isinstance(valor, str):
                valor = float(valor.replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
            
            db.executar_query(query, (descricao, categoria, valor, data, obs))
            log_info(f"Nova despesa lançada: {descricao} - R$ {valor}")
            return True
        except Exception as e:
            log_erro("Erro ao lançar despesa", e)
            return False

    @staticmethod
    def buscar_despesas():
        # CORREÇÃO 2: Query completa e chamando a função com ()
        # Antes estava retornando o objeto método, por isso dava erro de iterável
        query = "SELECT id, data_despesa, descricao, categoria, valor FROM despesas ORDER BY data_despesa DESC"
        return db.buscar_todos(query) 

    @staticmethod
    def excluir_despesa(id_despesa):
        try:
            # CORREÇÃO 3: Vírgula na tupla (id_despesa,)
            db.executar_query("DELETE FROM despesas WHERE id=?", (id_despesa,))
            return True
        except Exception as e:
            log_erro("Erro ao excluir despesa", e)
            return False

    @staticmethod
    def get_balanco_geral():
        try:
            # CORREÇÃO 4: Status 'Concluído' (Singular, conforme o resto do sistema)
            sql_receita = "SELECT SUM(valor) FROM servicos WHERE status = 'Concluído'"
            res_receita = db.buscar_um(sql_receita)
            total_receita = res_receita[0] if res_receita and res_receita[0] else 0.0

            sql_despesa = "SELECT SUM(valor) FROM despesas"
            res_despesa = db.buscar_um(sql_despesa)
            total_despesa = res_despesa[0] if res_despesa and res_despesa[0] else 0.0

            saldo = total_receita - total_despesa
            
            return total_receita, total_despesa, saldo
        except Exception as e:
            log_erro("Erro ao calcular balanço", e)
            return 0.0, 0.0, 0.0
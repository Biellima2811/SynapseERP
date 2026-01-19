from database.db_manager import db
from core.logger import log_erro, log_info
from datetime import datetime

class OSModel:
    
    @staticmethod
    def salvar(cliente_nome, equipamento, defeito, valor, status, prioridade, tecnico, obs):
        query = """
        INSERT INTO servicos (cliente_nome, equipamento, defeito, valor, status, prioridade, tecnico, observacoes) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            if isinstance(valor, str):
                valor = float(valor.replace("R$", "").replace(",", ".").strip() or 0)
                
            cursor = db.executar_query(query, (cliente_nome, equipamento, defeito, valor, status, prioridade, tecnico, obs))
            
            # --- NOVO: Gera Protocolo de Criação ---
            if cursor:
                id_gerado = cursor.lastrowid
                OSModel.registrar_protocolo(id_gerado, f"OS Aberta. Status: {status}. Técnico: {tecnico}")
                log_info(f"Nova OS criada: #{id_gerado}")
                return True
            return False
        except Exception as e:
            log_erro("Erro ao salvar OS", e)
            return False

    @staticmethod
    def buscar_todos():
        # Query ajustada para trazer a data correta
        query = "SELECT id, cliente_nome, equipamento, defeito, data_entrada, status, valor, prioridade FROM servicos ORDER BY id DESC"
        return db.buscar_todos(query)

    @staticmethod
    def buscar_por_id(id_os):
        query = "SELECT * FROM servicos WHERE id = ?"
        return db.buscar_um(query, (id_os,))

    @staticmethod
    def atualizar(id_os, tecnico, status, defeito, valor, obs, laudo):
        # CORREÇÃO AQUI: Adicionado o sinal de = (era 'where id?')
        query = """
        UPDATE servicos 
        SET tecnico=?, status=?, defeito=?, valor=?, observacoes=?, laudo=?
        WHERE id=?
        """
        try:
            if isinstance(valor, str):
                valor = float(valor.replace("R$", "").replace(",", ".").strip() or 0)

            db.executar_query(query, (tecnico, status, defeito, valor, obs, laudo, id_os))
            
            # --- NOVO: Gera Protocolo de Alteração ---
            OSModel.registrar_protocolo(id_os, f"Atualização de Status: {status}. Técnico: {tecnico}")
            
            log_info(f"OS #{id_os} atualizada com sucesso.")
            return True
        except Exception as e:
            log_erro(f"Erro ao atualizar OS #{id_os}", e)
            return False

    # --- MÉTODO NOVO: SISTEMA DE PROTOCOLOS ---
    @staticmethod
    def registrar_protocolo(id_os, acao, usuario="Admin"):
        """Grava no histórico quem fez o que e quando"""
        query = """
        INSERT INTO protocolos (os_id, acao, usuario)
        VALUES (?, ?, ?)
        """
        try:
            db.executar_query(query, (id_os, acao, usuario))
        except Exception as e:
            log_erro("Erro ao gerar protocolo", e)

    @staticmethod
    def buscar_historico(id_os):
        """Busca toda a capivara da OS"""
        query = "SELECT data_hora, acao, usuario FROM protocolos WHERE os_id = ? ORDER BY id DESC"
        return db.buscar_todos(query, (id_os,))
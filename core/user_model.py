from database.db_manager import db
from core.security import SecurityAuth
from core.logger import log_erro, log_info

class UserModel:

    @staticmethod
    def salvar(usuario, senha, nivel):
        try:
            hash_obj = SecurityAuth.criar_hash_senha(senha)
            senha_hash = hash_obj.decode('utf-8')
        except Exception as e:
            log_erro(f'Erro ao gerar hash: {e}')
            return False
        
        query = """INSERT INTO usuarios (usuario, senha_hash, nivel, ativo)
                    VALUES (?, ?, ?, 1)"""
        try:
            db.executar_query(query, (usuario, senha_hash, nivel))
            log_info(f'Operação - Usuário: {usuario} criado com nível {nivel}!')
            return True
        except Exception as e:
            log_erro(f'Erro ao criar usuário! - MSG: {e}')
            return False
    
    @staticmethod
    def buscar_todos():
        return db.buscar_todos('SELECT id, usuario, nivel, ativo FROM usuarios')
    
    @staticmethod
    def atualizar(id_user, usuario, nivel, nova_senha=None):
        try:
            if nova_senha:
                # Se trocou a senha, gera hash novo
                hash_obj = SecurityAuth.criar_hash_senha(nova_senha)
                senha_hash = hash_obj.decode('utf-8')

                query = """UPDATE usuarios SET usuario=?, nivel=?, senha_hash=?
                            WHERE id=?"""
                db.executar_query(query, (usuario, nivel, senha_hash, id_user))
            else:
                # Só atualiza dados cadastrais
                query = 'UPDATE usuarios SET usuario=?, nivel=? WHERE id=?'
                # CORREÇÃO CRÍTICA: Removido os parenteses extras que transformavam a query em função
                db.executar_query(query, (usuario, nivel, id_user))
            
            log_info(f'Usuário: {id_user} atualizado!')
            return True
        except Exception as e:
            log_erro(f'Erro ao atualizar usuário! - MSG: {e}')
            return False
    
    @staticmethod
    def excluir(id_user):
        try:
            # Verifica se não é o último admin
            admins = db.buscar_todos("SELECT count(*) FROM usuarios WHERE nivel='admin'")
            target = db.buscar_um("SELECT nivel FROM usuarios WHERE id=?", (id_user,))

            # Se for admin e só tiver 1 admin no sistema, bloqueia
            if target and target[0] == 'admin' and admins[0][0] <= 1:
                log_info('Tentativa de excluir o último admin bloqueada')
                return False
            
            # CORREÇÃO CRÍTICA: Tabela 'usuarios' (plural) e tupla no parametro (id_user,)
            db.executar_query('DELETE FROM usuarios WHERE id=?', (id_user,))
            
            log_info(f'Usuário: {id_user}, foi excluído da base')
            return True
        except Exception as e:
            log_erro(f'Erro na execução de exclusão do usuário, MSG: {e}')
            return False
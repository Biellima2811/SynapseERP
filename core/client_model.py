from database.db_manager import db

class ClienteModel:

    @staticmethod
    def adicionar(nome, cpf_cnpj, telefone, cidade):
        # Insere um novo cliente no banco
        query = """insert into clientes (nome, cpf_cnpj, telefone, endereco)
        values (?,?,?,?)"""
        # Obs: Estamos usando o campo 'endereco' para guardar a Cidade por enquanto
        try:
            db.executar_query(query, (nome, cpf_cnpj, telefone, cidade))
            return True
        except Exception as e:
            print(f'Erro ao adicionar cliente: {e}')
            return False
    
    @staticmethod
    def buscar_todos():
        # Retorna lista de todos os clientes
        query = """select id, nome, cpf_cnpj, telefone, endereco 
                    from clientes
                    order by id desc"""
        return db.buscar_todos(query)
    
    @staticmethod
    def buscar_por_nome(termo):
        # Filtra clientes pro nome ou cpf
        termo = f'%{termo}%'
        query = """
                select id, nome, cpf_cnpj, telefone, endereco
                from clientes
                where nome like ? or cpf_cnpj like ?"""
        return db.buscar_todos(query, (termo, termo))
    
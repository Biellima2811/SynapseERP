import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="synapse.db"): # Nome do banco atualizado
        if not os.path.exists("data"):
            os.makedirs("data")
            
        self.db_path = os.path.join("data", db_name)
        self.inicializar_tabelas()
        self.migrar_banco() # Verifica se precisa adicionar colunas novas

    def get_conexao(self):
        return sqlite3.connect(self.db_path)

    def inicializar_tabelas(self):
        sql_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            nivel TEXT DEFAULT 'operador',
            ativo INTEGER DEFAULT 1
        );
        """
        # Tabela Clientes Base
        sql_clientes = """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf_cnpj TEXT,
            telefone TEXT,
            email TEXT,
            cep TEXT,
            endereco TEXT,
            numero TEXT,
            bairro TEXT,
            cidade TEXT,
            uf TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        # Tabela OS Base
        sql_servicos = """
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            cliente_nome TEXT,
            equipamento TEXT,
            defeito TEXT,
            observacoes TEXT,
            tecnico TEXT,
            prioridade TEXT DEFAULT 'Normal',
            status TEXT DEFAULT 'Aberto',
            valor REAL DEFAULT 0.0,
            data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        );
        """
        sql_protocolos = """
        CREATE TABLE IF NOT EXISTS protocolos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            os_id INTEGER,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            acao TEXT,
            usuario TEXT,
            FOREIGN KEY(os_id) REFERENCES servicos(id)
        ); 
        """
        self.executar_query(sql_protocolos)
        self.executar_query(sql_usuarios)
        self.executar_query(sql_clientes)
        self.executar_query(sql_servicos)

    def migrar_banco(self):
        """Adiciona colunas novas caso o banco seja antigo"""
        # Lista de Colunas Novas para garantir que existam
        # Tabela: (Coluna, Tipo)
        colunas_novas = {
            'clientes': [('email', 'TEXT'), ('cep', 'TEXT'), ('bairro', 'TEXT'), ('uf', 'TEXT'), ('numero', 'TEXT'), ('endereco', 'TEXT')],
            'servicos': [('observacoes', 'TEXT'), ('tecnico', 'TEXT'), ('prioridade', 'TEXT'), ('laudo', 'TEXT')]
        }
        
        try:
            with self.get_conexao() as conn:
                cursor = conn.cursor()
                for tabela, colunas in colunas_novas.items():
                    # Pega colunas atuais
                    cursor.execute(f"PRAGMA table_info({tabela})")
                    existentes = [col[1] for col in cursor.fetchall()]
                    
                    for nova_col, tipo in colunas:
                        if nova_col not in existentes:
                            print(f"Migrando BD: Adicionando {nova_col} em {tabela}...")
                            cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {nova_col} {tipo}")
                conn.commit()
        except Exception as e:
            print(f"Erro na migração: {e}")

    def executar_query(self, query, parametros=()):
        try:
            with self.get_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(query, parametros)
                conn.commit()
                return cursor
        except Exception as e:
            print(f"ERRO CRÍTICO NO BANCO: {e}")
            return None

    def buscar_todos(self, query, parametros=()):
        with self.get_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            return cursor.fetchall()

    def buscar_um(self, query, parametros=()):
        with self.get_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            return cursor.fetchone()

db = DatabaseManager()
import bcrypt
from database.db_manager import db 

class SecurityAuth:
    
    @staticmethod
    def criar_hash_senha(senha_pura):
        # Garante que seja string antes de codificar
        if not isinstance(senha_pura, str):
            senha_pura = str(senha_pura)
        bytes_senha = senha_pura.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_senha = bcrypt.hashpw(bytes_senha, salt)
        return hash_senha
    
    @staticmethod
    def verificar_senha(senha_pura, hash_banco):
        bytes_senha = senha_pura.encode('utf-8')
        if isinstance(hash_banco, str):
            hash_banco = hash_banco.encode('utf-8')
        
        return bcrypt.checkpw(bytes_senha, hash_banco)
    
    @staticmethod
    def criar_admin_padrao():
        """Cria o usuário Admin/admin123 se o banco estiver vazio"""
        # Aqui 'db' agora é o objeto correto, então buscar_um funciona
        usuario = db.buscar_um("SELECT * FROM usuarios WHERE usuario = ?", ('admin',))

        if not usuario:
            print('⚠️ CRIANDO USUÁRIO ADMIN PADRÃO...')
            hash_seguro = SecurityAuth.criar_hash_senha('admin123')
            
            # CORREÇÃO: utf-8 (estava uft-8) e separação correta dos parâmetros
            sql = "INSERT INTO usuarios (usuario, senha_hash, nivel) VALUES (?,?,?)"
            params = ('admin', hash_seguro.decode('utf-8'), 'admin')
            
            db.executar_query(sql, params)
            print("✅ Usuário 'admin' criado com senha 'admin123'.")
    
    @staticmethod
    def login(usuario, senha):
        """Tenta logar e retorna True/False"""
        dados_user = db.buscar_um('SELECT senha_hash FROM usuarios WHERE usuario = ?', (usuario,))

        if dados_user:
            hash_salvo = dados_user[0]
            if SecurityAuth.verificar_senha(senha, hash_salvo):
                return True
        return False
    
    @staticmethod
    def verificar_nivel(usuario):
        # Retorna o nuvel de acesso (ex: admin, tecnico):
        dados = db.buscar_um("select nivel from usuarios where usuario = ?", (usuario,))
        if dados:
            return dados[0]
        return 'operador'
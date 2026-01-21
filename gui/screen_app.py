import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.screen_dashboard import DashboardScreen
from gui.screen_clients import ClientesScreen
from gui.screen_os import OSScreen
from gui.screen_users import UsersScreen
from gui.screen_finance import FinanceScreen
from tkinter import messagebox

class MainAppScreen(ttk.Frame):
    # Recebe nivel_acesso agora
    def __init__(self, parent, usuario_logado, nivel_acesso):
        super().__init__(parent)
        self.pack(fill=BOTH, expand=YES)
        
        self.parent = parent
        self.usuario_logado = usuario_logado
        self.nivel_acesso = nivel_acesso # Guarda o nível
        
        # --- TOPBAR ---
        topbar = ttk.Frame(self, bootstyle='primary', padding=10)
        topbar.pack(side=TOP, fill=X)

        ttk.Label(topbar, text="Synapse ERP", font=("Calibri", 18, "bold"), bootstyle="inverse-primary").pack(side=LEFT, padx=10)
        # Mostra quem está logado e o nível
        ttk.Label(topbar, text=f"Usuário: {usuario_logado} | Nível: {nivel_acesso.upper()}", font=("Calibri", 10), bootstyle="inverse-primary").pack(side=RIGHT, padx=10)

        # --- CONTAINER ---
        container = ttk.Frame(self)
        container.pack(side=LEFT, fill=Y)

        # --- SIDEBAR ---
        self.sidebar = ttk.Frame(container, width=220, bootstyle='light')
        self.sidebar.pack(side=LEFT, fill=Y)

        # --- CONTEÚDO ---
        self.content_area = ttk.Frame(container, padding=20)
        self.content_area.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.criar_menu()
        self.trocar_tela(DashboardScreen)
    
    def criar_menu(self):
        ttk.Label(self.sidebar, text="NAVEGAÇÃO", font=("Calibri", 10, "bold"), bootstyle="secondary").pack(anchor=W, padx=20, pady=(20, 10))

        # Lista padrão
        self.criar_botao("📊  Dashboard", DashboardScreen)
        self.criar_botao("👥  Clientes", ClientesScreen)
        if self.nivel_acesso in ['admin', 'gerente']:
            self.criar_botao("💰  Financeiro", FinanceScreen)
        self.criar_botao("🛠️  Serviços/OS", OSScreen)

        # SE FOR ADMIN, MOSTRA O BOTÃO DE SEGURANÇA
        if self.nivel_acesso == 'admin':
            self.criar_botao("🔐  Usuários", UsersScreen)

        # Botão Sair
        ttk.Separator(self.sidebar).pack(fill=X, padx=20, pady=20)
        ttk.Button(self.sidebar, text='Sair / Logout', bootstyle="danger-outline", command=self.logout).pack(side=BOTTOM, fill=X, padx=20, pady=20)

    def criar_botao(self, texto, classe_tela):
        btn = ttk.Button(
            self.sidebar,
            text=texto,
            bootstyle='light',
            command=lambda: self.trocar_tela(classe_tela)
        )
        btn.pack(fill=X, padx=5, pady=2)
    
    def trocar_tela(self, classe_tela):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        tela = classe_tela(self.content_area)
        tela.pack(fill=BOTH, expand=YES)

    def logout(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            self.master.destroy()
            # O correto seria reiniciar o app, mas destruir fecha a janela e encerra o script.
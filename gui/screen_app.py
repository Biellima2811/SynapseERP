import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.screen_dashboard import DashboardScreen
from gui.screen_clients import ClientesScreen
from gui.screen_os import OSScreen

class MainAppScreen(ttk.Frame):
    def __init__(self, parent, usuario_logado):
        super().__init__(parent)
        self.pack(fill=BOTH, expand=YES)
        self.parent = parent

        # --- TOPBAR (Barra Superior) ---
        topbar = ttk.Frame(self, bootstyle='primary', padding=10)
        topbar.pack(side=TOP, fill=X)

        ttk.Label(topbar, text="GUARDIÃO ERP", font=("Calibri", 18, "bold"), bootstyle="inverse-primary").pack(side=LEFT, padx=10)
        ttk.Label(topbar, text=f"Usuário: {usuario_logado}", font=("Calibri", 10), bootstyle="inverse-primary").pack(side=RIGHT, padx=10)

        # --- CONTAINER PRINCIPAL ---
        container = ttk.Frame(self)
        container.pack(side=LEFT, fill=Y)

        # --- SIDEBAR (Menu Lateral) ---
        self.sidebar = ttk.Frame(container, width=220, bootstyle='light')
        self.sidebar.pack(side=LEFT, fill=Y)

        # --- ÁREA DE CONTEÚDO ---
        self.content_area = ttk.Frame(container, padding=20)
        self.content_area.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Montar o menu
        self.criar_menu()

        # Iniciar no Dashboard
        self.trocar_tela(DashboardScreen)
    
    def criar_menu(self):
        ttk.Label(self.sidebar, text="NAVEGAÇÃO", font=("Calibri", 10, "bold"), bootstyle="secondary").pack(anchor=W, padx=20, pady=(20, 10))

        # Lista de Botões
        # (Texto, Classe da Tela)
        menus = [
            ("📊  Dashboard", DashboardScreen),
            ("👥  Clientes", ClientesScreen), # Faremos depois
            ("🛒  Vendas", None),
            ("🛠️  Serviços/OS", OSScreen),
            ("💰  Financeiro", None),
        ]
        for texto, classe_tela in menus:
            btn = ttk.Button(
                self.sidebar,
                text=texto,
                bootstyle='light',
                # Se tiver classe, troca. Se for None, não faz nada (por enquanto)
                command=lambda c=classe_tela: self.trocar_tela(c) if c else print("Em breve")   
            )
            btn.pack(fill=X, padx=5, pady=2)

        # Botão Sair
        ttk.Separator(self.sidebar).pack(fill=X, padx=20, pady=20)

        ttk.Button(self.sidebar, 
                   text='Sair / Logout', 
                   bootstyle="danger-outline", 
                   command=self.logout).pack(side=BOTTOM, fill=X, padx=20, pady=20)
    
    def trocar_tela(self, classe_tela):
        # Limpa a área atual
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
        # Cria a nova tela
        tela = classe_tela(self.content_area)
        tela.pack(fill=BOTH, expand=YES)

    def logout(self):
        # Destrói a tela principal e volta pro login
        self.destroy()
        self.parent.mostrar_login()
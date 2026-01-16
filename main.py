import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from core.security import SecurityAuth
from gui.screen_login import LoginScreen
from gui.screen_app import MainAppScreen 
import os 

class GuardiaoApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Guardião ERP - Sistema Integrado")
        self.geometry("1280x720")
        
        # --- CONFIGURAÇÃO DO ÍCONE (.ico) ---
        # O método iconbitmap é específico para arquivos .ico no Windows
        caminho_icone = "assets/logo_guardiao.ico"
        if os.path.exists(caminho_icone):
            try:
                self.iconbitmap(caminho_icone)
            except Exception as e:
                print(f"Erro ao carregar ícone: {e}")

        # Variáveis de monitoramento (Timeout de segurança)
        self.tempo_limite = 5 * 60 * 1000 # 5 minutos
        self.id_timer = None

        # Monitora atividade
        self.bind_all('<Any-KeyPress>', self.resetar_timer)
        self.bind_all('<Any-ButtonPress>', self.resetar_timer)
        self.bind_all('<Motion>', self.resetar_timer)

        # Inicializa
        SecurityAuth.criar_admin_padrao()
        self.mostrar_login()

    def mostrar_login(self):
        if self.id_timer:
            self.after_cancel(self.id_timer)
            self.id_timer = None
        self.login = LoginScreen(self, on_login_success=self.iniciar_sistema)

    def iniciar_sistema(self):
        self.state('zoomed')
        self.title("Guardião ERP - Painel Principal")
        self.app = MainAppScreen(self, usuario_logado="Admin")
        self.resetar_timer()

    def resetar_timer(self, event=None):
        if not hasattr(self, 'app') or not self.app.winfo_exists():
            return
        if self.id_timer:
            self.after_cancel(self.id_timer)
        self.id_timer = self.after(self.tempo_limite, self.realizar_logoff_automatico)
    
    def realizar_logoff_automatico(self):
        if hasattr(self, 'app') and self.app.winfo_exists():
            self.app.destroy()
            self.mostrar_login()
            messagebox.showwarning('Segurança', "Sessão expirada por inatividade.")

if __name__ == "__main__":
    app = GuardiaoApp()
    app.mainloop()
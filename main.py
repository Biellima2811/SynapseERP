import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from core.security import SecurityAuth
from gui.screen_login import LoginScreen
from gui.screen_app import MainAppScreen
import os 
from core.logger import log_info, log_erro


class SynapseApp(ttk.Window): # Nome da classe atualizado
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("SynapseERP - Sistema Integrado")
        self.geometry("1280x720")
        
        # Log de inicialização
        log_info("Sistema SynapseERP iniciado.")
        
        # Ícone
        icones_possiveis = ["assets/SynapseERP.ico"]
        
        for icone in icones_possiveis:
            if os.path.exists(icone):
                try:
                    self.iconbitmap(icone)
                    log_info(f"Ícone carregado: {icone}")
                    break
                except Exception as e:
                    log_erro("Erro no ícone", e)

        # Timeout
        self.tempo_limite = 10 * 60 * 1000 # Aumentei para 10 min (padrão melhor)
        self.id_timer = None

        self.bind_all('<Any-KeyPress>', self.resetar_timer)
        self.bind_all('<Any-ButtonPress>', self.resetar_timer)
        self.bind_all('<Motion>', self.resetar_timer)

        SecurityAuth.criar_admin_padrao()
        self.mostrar_login()

    def mostrar_login(self):
        if self.id_timer:
            self.after_cancel(self.id_timer)
            self.id_timer = None
        self.login = LoginScreen(self, on_login_success=self.iniciar_sistema)

    def iniciar_sistema(self, usuario, nivel):
        log_info(f"Login realizado: {usuario} [{nivel}]")
        self.state('zoomed')
        self.title(f"SynapseERP - Logado como: {usuario}")
        # Passa os dados para a tela principal
        self.app = MainAppScreen(self, usuario_logado=usuario, nivel_acesso=nivel)
        self.resetar_timer()

    def resetar_timer(self, event=None):
        if not hasattr(self, 'app') or not self.app.winfo_exists():
            return
        if self.id_timer:
            self.after_cancel(self.id_timer)
        self.id_timer = self.after(self.tempo_limite, self.realizar_logoff_automatico)
    
    def realizar_logoff_automatico(self):
        if hasattr(self, 'app') and self.app.winfo_exists():
            log_info("Sessão expirada por inatividade.")
            self.app.destroy()
            self.mostrar_login()
            messagebox.showwarning('Segurança', "Sessão expirada por inatividade.")

if __name__ == "__main__":
    app = SynapseApp()
    app.mainloop()
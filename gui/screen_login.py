import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from core.security import SecurityAuth
from tkinter import messagebox
from PIL import Image, ImageTk 
import os

class LoginScreen(ttk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.pack(fill=BOTH, expand=YES)
        self.on_login_success = on_login_success

        # --- LAYOUT DIVIDIDO (SPLIT SCREEN) ---
        
        # 1. LADO ESQUERDO (Branding / Marca)
        self.left_side = ttk.Frame(self, bootstyle="primary")
        self.left_side.pack(side=LEFT, fill=BOTH, expand=YES)
        
        left_content = ttk.Frame(self.left_side, bootstyle="primary")
        left_content.place(relx=0.5, rely=0.5, anchor=CENTER)

        # --- CARREGAMENTO DE IMAGEM ROBUSTO ---
        # 1. Descobre onde este arquivo (screen_login.py) está
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # 2. Sobe um nível para ir para a pasta raiz (Guardiao-ERP)
        diretorio_raiz = os.path.dirname(diretorio_atual)
        # 3. Monta o caminho final para assets/SynapseERP.png
        caminho_logo = os.path.join(diretorio_raiz, "assets", "SynapseERP.png")

        # Debug: Imprime no terminal onde ele está procurando (ajuda a achar erros)
        print(f"Procurando imagem em: {caminho_logo}")

        if os.path.exists(caminho_logo):
            try:
                # Abre e Redimensiona
                pil_img = Image.open(caminho_logo)
                # Redimensiona para ficar bonito (LANCZOS é o melhor filtro de qualidade)
                pil_img = pil_img.resize((550, 500), Image.Resampling.LANCZOS) 
                self.logo_img = ImageTk.PhotoImage(pil_img)
                
                # Exibe a imagem
                ttk.Label(left_content, image=self.logo_img, bootstyle="inverse-primary").pack(pady=(0, 20))
            except Exception as e:
                print(f"Erro ao processar imagem: {e}")
                ttk.Label(left_content, text="[Imagem não carregada]", bootstyle="inverse-primary").pack()
        else:
            print("ERRO: Arquivo de imagem não encontrado!")
            # Se não achar a imagem, mostra um texto substituto
            ttk.Label(left_content, text="[Logo Aqui]", bootstyle="inverse-primary").pack(pady=20)
        
        #ttk.Label(left_content, text="GUARDIÃO ERP", font=("Calibri", 30, "bold"), bootstyle="inverse-primary").pack()
        ttk.Label(left_content, text="Gestão Inteligente e Segura", font=("Calibri", 12, "italic"), bootstyle="inverse-primary").pack(pady=5)

        # --- LADO DIREITO (Formulário) ---
        self.right_side = ttk.Frame(self, bootstyle="light")
        self.right_side.pack(side=RIGHT, fill=BOTH, expand=YES)

        login_frame = ttk.Frame(self.right_side, padding=40)
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=350)

        ttk.Label(login_frame, text="Bem-vindo", font=("Calibri", 26, "bold"), bootstyle="primary").pack(anchor=W)
        ttk.Label(login_frame, text="Faça login para continuar", font=("Calibri", 10), bootstyle="secondary").pack(anchor=W, pady=(0, 30))

        ttk.Label(login_frame, text="Usuário", bootstyle="primary").pack(anchor=W)
        self.entry_user = ttk.Entry(login_frame)
        self.entry_user.pack(fill=X, pady=(5, 15))
        self.entry_user.focus()

        ttk.Label(login_frame, text="Senha", bootstyle="primary").pack(anchor=W)
        self.entry_pass = ttk.Entry(login_frame, show="•")
        self.entry_pass.pack(fill=X, pady=(5, 20))
        self.entry_pass.bind('<Return>', lambda e: self.fazer_login())

        btn = ttk.Button(login_frame, text="ENTRAR", bootstyle="primary", command=self.fazer_login)
        btn.pack(fill=X, pady=10)
        
        ttk.Label(login_frame, text="© 2026 Synapse Systems", font=("Arial", 8), bootstyle="secondary").pack(pady=(20, 0))

    def fazer_login(self):
        user = self.entry_user.get()
        senha = self.entry_pass.get()

        if SecurityAuth.login(user, senha):
            # NOVO: Busca o nível para passar adiante
            nivel = SecurityAuth.verificar_nivel(user)
            self.destroy()
            # Passamos usuário e nível
            self.on_login_success(user, nivel) 
        else:
            messagebox.showerror("Acesso Negado", "Credenciais incorretas.")
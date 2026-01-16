import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from core.client_model import ClienteModel

class AddClientePopup(ttk.Toplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.title("Novo Cadastro de Cliente")
        self.geometry("600x450") # Um pouco mais largo para acomodar o grid
        self.resizable(False, False)
        self.on_confirm = on_confirm
        
        self.position_center()

        # --- CONTAINER PRINCIPAL ---
        # Criamos um frame para segurar o grid com padding
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=BOTH, expand=YES)

        # Configuração das Colunas do Grid (para ficarem proporcionais)
        # Coluna 0 e Coluna 1 terão o mesmo peso (50% cada)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # --- LINHA 0: Título ---
        ttk.Label(frame, text="Dados do Cliente", font=("Calibri", 16, "bold"), bootstyle="primary").grid(
            row=0, column=0, columnspan=2, sticky=W, pady=(0, 20)
        )

        # --- LINHA 1: Nome (Ocupa as 2 colunas) ---
        ttk.Label(frame, text="Nome Completo / Razão Social *").grid(row=1, column=0, columnspan=2, sticky=W)
        self.entry_nome = ttk.Entry(frame)
        self.entry_nome.grid(row=2, column=0, columnspan=2, sticky=EW, pady=(5, 15))

        # --- LINHA 2: CPF e Telefone (Lado a Lado) ---
        
        # Coluna 0: CPF
        ttk.Label(frame, text="CPF / CNPJ").grid(row=3, column=0, sticky=W)
        self.entry_cpf = ttk.Entry(frame)
        self.entry_cpf.grid(row=4, column=0, sticky=EW, pady=(5, 15), padx=(0, 10)) # padx na direita para separar

        # Coluna 1: Telefone
        ttk.Label(frame, text="Telefone (WhatsApp)").grid(row=3, column=1, sticky=W)
        self.entry_tel = ttk.Entry(frame)
        self.entry_tel.grid(row=4, column=1, sticky=EW, pady=(5, 15))

        # --- LINHA 3: Cidade ---
        ttk.Label(frame, text="Cidade").grid(row=5, column=0, columnspan=2, sticky=W)
        self.entry_cidade = ttk.Entry(frame)
        self.entry_cidade.grid(row=6, column=0, columnspan=2, sticky=EW, pady=(5, 20))

        # --- LINHA 4: Botão Salvar ---
        ttk.Button(frame, text="SALVAR CADASTRO", bootstyle="success", command=self.salvar).grid(
            row=7, column=0, columnspan=2, sticky=EW, pady=10
        )
        
        # Aviso
        ttk.Label(frame, text="* Campos Obrigatórios", bootstyle="secondary", font=("Arial", 8)).grid(
            row=8, column=0, columnspan=2
        )

    def salvar(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        tel = self.entry_tel.get().strip()
        cidade = self.entry_cidade.get().strip()

        if not nome:
            Messagebox.show_error("O campo Nome é obrigatório!", "Erro de Validação")
            self.lift() # Traz a janela para frente se der erro
            return

        # Tenta salvar
        if ClienteModel.adicionar(nome, cpf, tel, cidade):
            Messagebox.show_info("Cliente cadastrado com sucesso!", "Sucesso")
            self.on_confirm() # Atualiza a tabela lá atrás
            self.destroy() # Fecha o popup
        else:
            Messagebox.show_error("Erro ao salvar no banco de dados.", "Erro Crítico")
            self.lift()

    def position_center(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
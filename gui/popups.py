import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from core.client_model import ClienteModel
from core.os_model import OSModel
from core.finance_model import FinanceModel
import json
import urllib.request # Para fazer a consulta na API ViaCEP

class AddClientePopup(ttk.Toplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.title("Novo Cliente - Completo")
        self.geometry("750x700") # Um pouquinho maior para caber tudo
        self.on_confirm = on_confirm
        self.position_center()

        frame = ttk.Frame(self, padding=25)
        frame.pack(fill=BOTH, expand=YES)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Dados Pessoais", font=("Calibri", 14, "bold"), bootstyle="primary").grid(row=0, columnspan=2, sticky=W, pady=10)

        # Nome
        self.criar_campo(frame, "Nome Completo *", 1, 0, 2)
        self.entry_nome = self.ultimo_entry

        # CPF e Telefone
        self.criar_campo(frame, "CPF / CNPJ", 3, 0)
        self.entry_cpf = self.ultimo_entry
        
        self.criar_campo(frame, "Telefone / WhatsApp", 3, 1)
        self.entry_tel = self.ultimo_entry

        # Email
        self.criar_campo(frame, "E-mail", 5, 0, 2)
        self.entry_email = self.ultimo_entry

        # --- SEÇÃO DE ENDEREÇO INTELIGENTE ---
        ttk.Separator(frame).grid(row=7, columnspan=2, sticky=EW, pady=15)
        ttk.Label(frame, text="Endereço (Busca Automática)", font=("Calibri", 14, "bold"), bootstyle="primary").grid(row=8, columnspan=2, sticky=W, pady=10)

        # LINHA DO CEP (Com botão de busca)
        frame_cep = ttk.Frame(frame)
        frame_cep.grid(row=9, column=0, sticky=EW, padx=5)
        
        ttk.Label(frame_cep, text="CEP").pack(anchor=W)
        self.entry_cep = ttk.Entry(frame_cep)
        self.entry_cep.pack(side=LEFT, fill=X, expand=YES)
        
        # Botão Lupa
        btn_busca = ttk.Button(frame_cep, text="🔍", bootstyle="info-outline", command=self.buscar_cep)
        btn_busca.pack(side=LEFT, padx=(5, 0))
        
        # Bind: Se apertar ENTER no campo CEP, também busca
        self.entry_cep.bind("<Return>", lambda e: self.buscar_cep())

        # UF (Estado) - Lado do CEP
        self.criar_campo(frame, "Estado (UF)", 9, 1)
        self.entry_uf = self.ultimo_entry

        # Logradouro e Número
        self.criar_campo(frame, "Logradouro (Rua/Av)", 11, 0) # Novo Campo
        self.entry_logradouro = self.ultimo_entry

        self.criar_campo(frame, "Número", 11, 1) # Novo Campo
        self.entry_numero = self.ultimo_entry

        # Bairro e Cidade
        self.criar_campo(frame, "Bairro", 13, 0)
        self.entry_bairro = self.ultimo_entry
        
        self.criar_campo(frame, "Cidade", 13, 1)
        self.entry_cidade = self.ultimo_entry

        # Botão Salvar
        ttk.Button(frame, text="SALVAR CADASTRO", bootstyle="success", command=self.salvar).grid(row=15, columnspan=2, sticky=EW, pady=30)

    def criar_campo(self, parent, texto, row, col, colspan=1):
        ttk.Label(parent, text=texto).grid(row=row, column=col, sticky=W, padx=5)
        entry = ttk.Entry(parent)
        entry.grid(row=row+1, column=col, columnspan=colspan, sticky=EW, padx=5, pady=(0, 10))
        self.ultimo_entry = entry

    def buscar_cep(self):
        """Consulta a API ViaCEP e preenche os campos"""
        cep = self.entry_cep.get().replace("-", "").replace(".", "").strip()
        
        if len(cep) != 8:
            Messagebox.show_error("CEP inválido! Digite 8 números.", "Erro")
            return

        url = f"https://viacep.com.br/ws/{cep}/json/"
        
        try:
            # Faz a requisição
            with urllib.request.urlopen(url) as response:
                dados = json.loads(response.read().decode())
                
            if "erro" in dados:
                Messagebox.show_warning("CEP não encontrado!", "Aviso")
                return
            
            # Preenche os campos (limpa antes para garantir)
            self.preencher_campo(self.entry_logradouro, dados.get("logradouro", ""))
            self.preencher_campo(self.entry_bairro, dados.get("bairro", ""))
            self.preencher_campo(self.entry_cidade, dados.get("localidade", ""))
            self.preencher_campo(self.entry_uf, dados.get("uf", ""))
            
            # Foca no número para agilizar
            self.entry_numero.focus()
            
        except Exception as e:
            Messagebox.show_error(f"Erro de conexão: {e}", "Erro")

    def preencher_campo(self, entry_widget, valor):
        entry_widget.delete(0, END)
        entry_widget.insert(0, valor)

    def salvar(self):
        dados = [
            self.entry_nome.get(), self.entry_cpf.get(), self.entry_tel.get(),
            self.entry_email.get(), self.entry_cep.get(), 
            self.entry_logradouro.get(), self.entry_numero.get(), # Novos campos
            self.entry_bairro.get(), self.entry_cidade.get(), self.entry_uf.get()
        ]
        
        if not dados[0]: 
            Messagebox.show_error("Nome é obrigatório!")
            return

        if ClienteModel.adicionar(*dados):
            Messagebox.show_info("Cliente Salvo com Sucesso!")
            self.on_confirm()
            self.destroy()
        else:
            Messagebox.show_error("Erro ao salvar no banco.")

    def position_center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x}+{y}')


# MANTENHA A CLASSE AddOSPopup IGUAL (Não precisa mexer nela agora)
class AddOSPopup(ttk.Toplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.title("Nova OS - Detalhada")
        self.geometry("850x700")
        self.on_confirm = on_confirm
        self.position_center()

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        # LINHA 1
        ttk.Label(frame, text="Cliente *").grid(row=0, column=0, sticky=W)
        self.cbo_cliente = ttk.Combobox(frame, values=self.get_clientes(), state="readonly")
        self.cbo_cliente.grid(row=1, column=0, columnspan=3, sticky=EW, pady=(0, 15))

        # LINHA 2
        ttk.Label(frame, text="Equipamento *").grid(row=2, column=0, sticky=W)
        self.entry_equip = ttk.Entry(frame)
        self.entry_equip.grid(row=3, column=0, sticky=EW, padx=(0, 5), pady=(0, 10))

        ttk.Label(frame, text="Marca / Modelo").grid(row=2, column=1, sticky=W)
        self.entry_marca = ttk.Entry(frame)
        self.entry_marca.grid(row=3, column=1, sticky=EW, padx=5, pady=(0, 10))

        ttk.Label(frame, text="Nº Série / IMEI").grid(row=2, column=2, sticky=W)
        self.entry_serial = ttk.Entry(frame)
        self.entry_serial.grid(row=3, column=2, sticky=EW, padx=5, pady=(0, 10))

        # LINHA 3
        ttk.Label(frame, text="Senha do Dispositivo").grid(row=4, column=0, sticky=W)
        self.entry_senha = ttk.Entry(frame)
        self.entry_senha.grid(row=5, column=0, sticky=EW, padx=(0, 5), pady=(0, 10))

        ttk.Label(frame, text="Prioridade").grid(row=4, column=1, sticky=W)
        self.cbo_prio = ttk.Combobox(frame, values=["Baixa", "Normal", "Alta", "URGENTE"], state="readonly")
        self.cbo_prio.current(1)
        self.cbo_prio.grid(row=5, column=1, sticky=EW, padx=5, pady=(0, 10))
        
        ttk.Label(frame, text="Acessórios").grid(row=4, column=2, sticky=W)
        self.entry_acessorios = ttk.Entry(frame)
        self.entry_acessorios.grid(row=5, column=2, sticky=EW, padx=5, pady=(0, 10))

        # LINHA 4
        ttk.Label(frame, text="Defeito Relatado *").grid(row=6, columnspan=3, sticky=W)
        self.entry_defeito = ttk.Entry(frame)
        self.entry_defeito.grid(row=7, columnspan=3, sticky=EW, pady=(0, 10))

        # LINHA 5
        ttk.Label(frame, text="Técnico Responsável").grid(row=8, column=0, sticky=W)
        self.entry_tec = ttk.Entry(frame)
        self.entry_tec.grid(row=9, column=0, sticky=EW, padx=(0, 5), pady=(0, 10))

        ttk.Label(frame, text="Status Inicial").grid(row=8, column=1, sticky=W)
        self.cbo_status = ttk.Combobox(frame, values=["Aberto", "Em Análise", "Aguardando Peça"], state="readonly")
        self.cbo_status.current(0)
        self.cbo_status.grid(row=9, column=1, sticky=EW, padx=5, pady=(0, 10))
        
        ttk.Label(frame, text="Previsão Entrega").grid(row=8, column=2, sticky=W)
        self.entry_data = ttk.DateEntry(frame)
        self.entry_data.grid(row=9, column=2, sticky=EW, padx=5, pady=(0, 10))

        # LINHA 6
        ttk.Label(frame, text="Observações Técnicas").grid(row=10, sticky=W)
        self.txt_obs = ttk.Text(frame, height=4)
        self.txt_obs.grid(row=11, columnspan=3, sticky=EW, pady=(0, 15))

        # LINHA 7
        ttk.Label(frame, text="Orçamento Estimado (R$)").grid(row=12, column=0, sticky=W)
        self.entry_valor = ttk.Entry(frame)
        self.entry_valor.insert(0, "0.00")
        self.entry_valor.grid(row=13, column=0, sticky=EW, padx=(0, 5))

        ttk.Button(frame, text="ABRIR NOVA OS", bootstyle="success", command=self.salvar).grid(row=14, columnspan=3, sticky=EW, pady=20)

    def get_clientes(self):
        try:
            return [c[1] for c in ClienteModel.buscar_todos()]
        except: return []

    def salvar(self):
        obs_completa = f"Marca: {self.entry_marca.get()} | Serial: {self.entry_serial.get()} | Senha: {self.entry_senha.get()} | Acessórios: {self.entry_acessorios.get()}\n\nObs: {self.txt_obs.get('1.0', END).strip()}"
        
        dados = {
            'cliente': self.cbo_cliente.get(),
            'equip': self.entry_equip.get(),
            'defeito': self.entry_defeito.get(),
            'valor': self.entry_valor.get(),
            'status': self.cbo_status.get(),
            'prioridade': self.cbo_prio.get(),
            'tecnico': self.entry_tec.get(),
            'obs': obs_completa
        }

        if not dados['cliente'] or not dados['equip']:
            Messagebox.show_error("Preencha Cliente e Equipamento!")
            return

        if OSModel.salvar(dados['cliente'], dados['equip'], dados['defeito'], dados['valor'], 
                          dados['status'], dados['prioridade'], dados['tecnico'], dados['obs']):
            Messagebox.show_info("OS Aberta com Sucesso!")
            self.on_confirm()
            self.destroy()
        else:
            Messagebox.show_error("Erro ao salvar OS.")

    def position_center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x}+{y}')

class EditOSPopup(ttk.Toplevel):
    def __init__(self, parent, on_confirm, id_os):
        super().__init__(parent)
        self.title(f"Gerenciar OS #{id_os} - SynapseERP")
        self.geometry("900x750") # Aumentei um pouco
        self.on_confirm = on_confirm
        self.id_os = id_os
        
        self.position_center()
        self.dados = OSModel.buscar_por_id(id_os)

        # --- SISTEMA DE ABAS (TABS) ---
        # Agora dividimos a tela em "Edição" e "Histórico"
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Aba 1: Detalhes (Onde edita)
        self.tab_detalhes = ttk.Frame(self.tabs, padding=20)
        self.tabs.add(self.tab_detalhes, text="📝 Detalhes & Edição")

        # Aba 2: Histórico (Onde vê os protocolos)
        self.tab_historico = ttk.Frame(self.tabs, padding=20)
        self.tabs.add(self.tab_historico, text="🕒 Histórico de Alterações")

        # --- CONSTRUÇÃO DA ABA DETALHES ---
        self.construir_aba_detalhes()
        
        # --- CONSTRUÇÃO DA ABA HISTÓRICO ---
        self.construir_aba_historico()

    def construir_aba_detalhes(self):
        frame = self.tab_detalhes
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # Cabeçalho Informativo
        info_frame = ttk.Labelframe(frame, text="Dados do Equipamento", padding=10, bootstyle="info")
        info_frame.grid(row=0, columnspan=2, sticky=EW, pady=(0, 20))
        
        ttk.Label(info_frame, text=f"Cliente: {self.dados[2]}", font=("Calibri", 12, "bold")).pack(anchor=W)
        ttk.Label(info_frame, text=f"Equipamento: {self.dados[3]} | Prioridade: {self.dados[7]}", font=("Calibri", 11)).pack(anchor=W)
        
        # Campos Editáveis
        ttk.Label(frame, text="Defeito Relatado").grid(row=1, columnspan=2, sticky=W)
        self.entry_defeito = ttk.Entry(frame)
        self.entry_defeito.insert(0, self.dados[4] or "")
        self.entry_defeito.grid(row=2, columnspan=2, sticky=EW, pady=(0, 10))

        ttk.Label(frame, text="Técnico Responsável").grid(row=3, column=0, sticky=W)
        self.entry_tec = ttk.Entry(frame)
        self.entry_tec.insert(0, self.dados[6] or "")
        self.entry_tec.grid(row=4, column=0, sticky=EW, padx=(0, 5), pady=(0, 10))

        ttk.Label(frame, text="Status Atual").grid(row=3, column=1, sticky=W)
        self.cbo_status = ttk.Combobox(frame, values=["Aberto", "Em Análise", "Aguardando Peça", "Concluído", "Cancelado"], state="readonly")
        self.cbo_status.set(self.dados[8] or "Aberto")
        self.cbo_status.grid(row=4, column=1, sticky=EW, padx=5, pady=(0, 10))

        ttk.Label(frame, text="Laudo Técnico (Obrigatório p/ Concluir)", bootstyle="success").grid(row=5, sticky=W)
        self.txt_laudo = ttk.Text(frame, height=5)
        laudo_atual = self.dados[11] if len(self.dados) > 11 else ""
        self.txt_laudo.insert("1.0", laudo_atual or "")
        self.txt_laudo.grid(row=6, columnspan=2, sticky=EW, pady=(0, 15))

        ttk.Label(frame, text="Observações Internas").grid(row=7, column=0, sticky=W)
        self.entry_obs = ttk.Entry(frame)
        self.entry_obs.insert(0, self.dados[5] or "")
        self.entry_obs.grid(row=8, column=0, sticky=EW, padx=(0, 5))

        ttk.Label(frame, text="Valor Final (R$)").grid(row=7, column=1, sticky=W)
        self.entry_valor = ttk.Entry(frame)
        self.entry_valor.insert(0, f"{self.dados[9]:.2f}")
        self.entry_valor.grid(row=8, column=1, sticky=EW, padx=5)

        ttk.Button(frame, text="SALVAR ALTERAÇÕES", bootstyle="primary", command=self.atualizar).grid(row=9, columnspan=2, sticky=EW, pady=30)

    def construir_aba_historico(self):
        # Busca o histórico do banco
        historico = OSModel.buscar_historico(self.id_os)
        
        if not historico:
            ttk.Label(self.tab_historico, text="Nenhum registro de alteração encontrado.").pack(pady=20)
            return

        # Cria uma linha do tempo (Timeline)
        timeline_frame = ttk.Frame(self.tab_historico)
        timeline_frame.pack(fill=BOTH, expand=YES)

        # Cabeçalho da tabela de histórico
        cols = ["Data/Hora", "Usuário", "Ação Realizada"]
        tree_hist = ttk.Treeview(timeline_frame, columns=cols, show="headings", height=10, bootstyle="secondary")
        
        tree_hist.column("Data/Hora", width=150, anchor=CENTER)
        tree_hist.column("Usuário", width=100, anchor=CENTER)
        tree_hist.column("Ação Realizada", width=400, anchor=W)
        
        for c in cols: tree_hist.heading(c, text=c)
        
        tree_hist.pack(fill=BOTH, expand=YES)

        for item in historico:
            # item = (data, acao, usuario) -> A ordem vem do SQL
            # SQL: SELECT data_hora, acao, usuario
            tree_hist.insert("", END, values=(item[0], item[2], item[1]))

    def atualizar(self):
        novo_status = self.cbo_status.get()
        laudo = self.txt_laudo.get("1.0", END).strip()
        
        if novo_status == "Concluído" and len(laudo) < 5:
            Messagebox.show_warning("Preencha o Laudo Técnico para concluir.", "Aviso")
            return

        if OSModel.atualizar(self.id_os, self.entry_tec.get(), novo_status, self.entry_defeito.get(), 
                             self.entry_valor.get(), self.entry_obs.get(), laudo):
            Messagebox.show_info("OS Atualizada com sucesso!")
            self.on_confirm()
            self.destroy()
        else:
            Messagebox.show_error("Erro ao atualizar.", "Erro")

    def position_center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x}+{y}')

class AddUserPopup(ttk.Toplevel):
    def __init__(self, parent, on_confirm, dados_edicao=None):
        super().__init__(parent)
        self.on_confirm = on_confirm
        self.dados_edicao = dados_edicao # Se vier preenchido, é edição
        
        titulo = "Editar Usuário" if dados_edicao else "Novo Usuário"
        self.title(titulo)
        self.geometry("400x350")
        self.position_center()
        
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        
        # Campos
        ttk.Label(frame, text="Nome de Usuário (Login)").pack(anchor=W)
        self.entry_user = ttk.Entry(frame)
        self.entry_user.pack(fill=X, pady=(5, 15))
        
        ttk.Label(frame, text="Nível de Acesso").pack(anchor=W)
        # Define os níveis disponíveis no sistema
        self.cbo_nivel = ttk.Combobox(frame, values=["admin", "gerente", "tecnico"], state="readonly")
        self.cbo_nivel.pack(fill=X, pady=(5, 15))
        
        lbl_senha = "Nova Senha (deixe em branco para manter)" if dados_edicao else "Senha"
        ttk.Label(frame, text=lbl_senha).pack(anchor=W)
        self.entry_senha = ttk.Entry(frame, show="*")
        self.entry_senha.pack(fill=X, pady=(5, 20))
        
        # Preenche se for edição
        if dados_edicao:
            self.entry_user.insert(0, dados_edicao[1])
            self.cbo_nivel.set(dados_edicao[2].lower())
            self.entry_user.configure(state="readonly") # Não deixa mudar o login
            
        btn_txt = "SALVAR ALTERAÇÕES" if dados_edicao else "CRIAR USUÁRIO"
        ttk.Button(frame, text=btn_txt, bootstyle="success", command=self.salvar).pack(fill=X)

    def salvar(self):
        user = self.entry_user.get()
        nivel = self.cbo_nivel.get()
        senha = self.entry_senha.get()
        
        from core.user_model import UserModel # Import local para evitar ciclo
        
        if self.dados_edicao:
            # Modo Edição
            id_user = self.dados_edicao[0]
            if UserModel.atualizar(id_user, user, nivel, senha if senha else None):
                Messagebox.show_info("Usuário atualizado!")
                self.on_confirm()
                self.destroy()
        else:
            # Modo Criação
            if not user or not senha or not nivel:
                Messagebox.show_error("Preencha todos os campos!")
                return
            
            if UserModel.salvar(user, senha, nivel):
                Messagebox.show_info("Usuário criado!")
                self.on_confirm()
                self.destroy()

    def position_center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x}+{y}')

class AddExpensePopup(ttk.Toplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.title("Lançar Nova Despesa")
        self.geometry("500x450")
        self.on_confirm = on_confirm
        self.position_center()
        
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        
        ttk.Label(frame, text="Nova Saída / Pagamento", font=("Calibri", 16, "bold"), bootstyle="danger").pack(anchor=W, pady=(0,20))
        
        # Descrição
        ttk.Label(frame, text="Descrição (Ex: Aluguel, Peças)").pack(anchor=W)
        self.entry_desc = ttk.Entry(frame)
        self.entry_desc.pack(fill=X, pady=(5, 15))
        
        # Categoria
        ttk.Label(frame, text="Categoria").pack(anchor=W)
        self.cbo_cat = ttk.Combobox(frame, values=["Custos Fixos", "Fornecedores", "Impostos", "Funcionários", "Outros"], state="readonly")
        self.cbo_cat.pack(fill=X, pady=(5, 15))
        
        # Valor e Data
        row = ttk.Frame(frame)
        row.pack(fill=X)
        
        col1 = ttk.Frame(row)
        col1.pack(side=LEFT, fill=X, expand=YES, padx=(0, 5))
        ttk.Label(col1, text="Valor (R$)").pack(anchor=W)
        self.entry_valor = ttk.Entry(col1)
        self.entry_valor.pack(fill=X, pady=5)
        
        col2 = ttk.Frame(row)
        col2.pack(side=LEFT, fill=X, expand=YES, padx=(5, 0))
        ttk.Label(col2, text="Data (AAAA-MM-DD)").pack(anchor=W)
        self.entry_data = ttk.DateEntry(col2, dateformat="%Y-%m-%d")
        self.entry_data.pack(fill=X, pady=5)
        
        # Botão
        ttk.Button(frame, text="LANÇAR SAÍDA", bootstyle="danger", command=self.salvar).pack(fill=X, pady=30)

    def salvar(self):
        desc = self.entry_desc.get()
        cat = self.cbo_cat.get()
        valor = self.entry_valor.get()
        data = self.entry_data.entry.get()
        
        if not desc or not valor:
            Messagebox.show_error("Preencha descrição e valor!")
            return
            
        if FinanceModel.adicionar_despesa(desc, cat, valor, data, ""):
            Messagebox.show_info("Despesa lançada!")
            self.on_confirm()
            self.destroy()
        else:
            Messagebox.show_error("Erro ao salvar.")

    def position_center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x}+{y}')
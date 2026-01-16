import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.popups import AddClientePopup
from core.client_model import ClienteModel

class ClientesScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=BOTH, expand=YES)

        # Cabeçalho
        cabecalho = ttk.Frame(self)
        cabecalho.pack(fill=X, pady=(0, 10))

        ttk.Label(cabecalho, text='Gestão de Clientes', font=('Calibri', 24, 'bold'), bootstyle='primary').pack(side=LEFT)

        btn_frame = ttk.Frame(cabecalho)
        btn_frame.pack(side=RIGHT)
        ttk.Button(btn_frame, text="🖨️ Imprimir", bootstyle='secondary-outline').pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text='+ Novo Cliente', bootstyle='success', command=self.abrir_popup_novo).pack(side=LEFT, padx=5)
        
        # Filtros
        filtro_frame = ttk.Labelframe(self, text='Filtros de Busca', padding=10, bootstyle='info')
        filtro_frame.pack(fill=X, pady=0)

        filtro_frame.columnconfigure(1, weight=1)
        ttk.Label(filtro_frame, text='Buscar:').grid(row=0, column=0, padx=5, sticky=W)
        ttk.Entry(filtro_frame, width=40).grid(row=0, column=1, padx=5, sticky=EW)
        
        ttk.Label(filtro_frame, text='Status:').grid(row=0, column=2, padx=5, sticky=W)
        cbo = ttk.Combobox(filtro_frame, values=['Todos', 'Ativos', 'Inadimplentes'], state='readonly', width=15)
        cbo.current(0)
        cbo.grid(row=0, column=3, padx=5)
        
        ttk.Button(filtro_frame, text='Pesquisar', bootstyle='primary').grid(row=0, column=4, padx=10)

        # Separador visual
        ttk.Separator(self, bootstyle="info").pack(fill=X, pady=0)

        # --- TABELA ---
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=YES, pady=0)

        colunas = ["ID", "Nome Completo", "CPF/CNPJ", "Telefone", "Cidade", "Status"]
        
        # CORREÇÃO AQUI: O pai agora é 'table_frame', não 'self'
        self.tree = ttk.Treeview(table_frame, columns=colunas, show='headings', bootstyle='info')

        self.tree.column('ID', width=50, anchor=CENTER)
        self.tree.column('Nome Completo', width=350, anchor=W)
        self.tree.column('CPF/CNPJ', width=150, anchor=CENTER)
        self.tree.column('Telefone', width=130, anchor=CENTER)
        self.tree.column('Cidade', width=150, anchor=W)
        self.tree.column('Status', width=100, anchor=CENTER)

        for col in colunas:
            self.tree.heading(col, text=col)

        # CORREÇÃO AQUI: A barra de rolagem também vai para o 'table_frame'
        sb = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        sb.pack(side=RIGHT, fill=Y)

        # Dados fake
        dados = [
            (1, "Supermercado Do Povo", "12.345.678/0001-99", "(11) 98888-7777", "São Paulo", "Ativo"),
            (2, "João da Silva", "111.222.333-44", "(21) 99999-0000", "Rio de Janeiro", "Inadimplente"),
            (3, "Padaria Estrela", "98.765.432/0001-10", "(31) 3333-2222", "Belo Horizonte", "Ativo"),
        ]
        for item in dados:
            self.tree.insert("", END, values=item)
        
        self.carregar_dados()
    
    def abrir_popup_novo(self):
        AddClientePopup(self, on_confirm=self.carregar_dados)

    def carregar_dados(self):
        # Limpa a tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Busca do Banco de Dados
        clientes = ClienteModel.buscar_todos()
        
        for cli in clientes:
            # cli = (id, nome, cpf, tel, endereco)
            # Precisamos adicionar o status "Ativo" manualmente por enquanto
            self.tree.insert("", END, values=(cli[0], cli[1], cli[2], cli[3], cli[4], "Ativo"))
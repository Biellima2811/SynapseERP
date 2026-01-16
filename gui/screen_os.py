import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class OSScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=BOTH, expand=YES)
        
        # Cabeçalho
        cabecalho = ttk.Frame(self)
        cabecalho.pack(fill=X, pady=(0, 10))

        ttk.Label(cabecalho, text='Controle de Serviços (OS)', font=('Calibri', 24, 'bold'), bootstyle='primary').pack(side=LEFT)
        
        btn_frame = ttk.Frame(cabecalho)
        btn_frame.pack(side=RIGHT)
        ttk.Button(btn_frame, text='+ Nova OS', bootstyle='success').pack(side=LEFT, padx=5)

        # Filtros
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=X, pady=(0, 5), anchor=W)

        ttk.Label(filter_frame, text='Filtrar Status:', font=("Calibri", 11, "bold")).pack(side=LEFT, padx=(0, 10))

        botoes = [("Todas", "secondary"), ("Abertas", "info"), ("Em Andamento", "warning"), ("Concluídas", "success")]
        for txt, cor in botoes:
            ttk.Button(filter_frame, text=txt, bootstyle=f"{cor}-outline").pack(side=LEFT, padx=2)
        
        # Separador
        ttk.Separator(self, bootstyle="secondary").pack(fill=X, pady=(5, 0))

        # --- TABELA ---
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=YES, pady=0)

        colunas = ["Nº OS", "Cliente", "Equipamento", "Status", "Valor"]
        
        # CORREÇÃO AQUI: table_frame
        self.tree = ttk.Treeview(table_frame, columns=colunas, show='headings', bootstyle='primary')
        
        self.tree.column('Nº OS', width=60, anchor=CENTER)
        self.tree.column('Cliente', width=250, anchor=W)
        self.tree.column('Equipamento', width=200, anchor=W)
        self.tree.column('Status', width=120, anchor=CENTER)
        self.tree.column('Valor', width=100, anchor=E)

        for col in colunas:
            self.tree.heading(col, text=col)
        
        # CORREÇÃO AQUI: table_frame
        sb = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        sb.pack(side=RIGHT, fill=Y)

        # Dados fake
        self.tree.insert("", END, values=("1024", "João Silva", "Notebook Dell", "Em Andamento", "R$ 0,00"))
        self.tree.insert("", END, values=("1025", "Maria Souza", "iPhone 13", "Abertas", "R$ 0,00"))
        self.tree.insert("", END, values=("1023", "Padaria Estrela", "Impressora Térmica", "Concluídas", "R$ 150,00"))
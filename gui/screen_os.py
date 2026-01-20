import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.popups import AddOSPopup, EditOSPopup
from core.os_model import OSModel
from core.pdf_manager import PDFManager
from ttkbootstrap.dialogs import Messagebox

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

        ttk.Button(btn_frame, text='🖨️ Imprimir', bootstyle='secondary-outline', command=self.imprimir_selecionada).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text='+ Nova OS', bootstyle='success', command=self.abrir_popup_os).pack(side=LEFT, padx=5)

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

        colunas = ["Nº OS", "Cliente", "Equipamento", "Defeito", "Prioridade", "Status", "Valor"]
        self.tree = ttk.Treeview(table_frame, columns=colunas, show='headings', bootstyle='primary')
        
        self.tree.column('Nº OS', width=50, anchor=CENTER)
        self.tree.column('Cliente', width=200, anchor=W)
        self.tree.column('Equipamento', width=150, anchor=W)
        self.tree.column('Defeito', width=200, anchor=W)
        self.tree.column('Prioridade', width=100, anchor=CENTER) # Nova coluna
        self.tree.column('Status', width=120, anchor=CENTER)
        self.tree.column('Valor', width=80, anchor=E)

        for col in colunas:
            self.tree.heading(col, text=col)
        
        self.tree.bind("<Double-1>", self.ao_clicar_duplo)

        sb = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        sb.pack(side=RIGHT, fill=Y)

        self.carregar_dados()

        # Dados fake
        self.tree.insert("", END, values=("1024", "João Silva", "Notebook Dell", "Em Andamento", "R$ 0,00"))
        self.tree.insert("", END, values=("1025", "Maria Souza", "iPhone 13", "Abertas", "R$ 0,00"))
        self.tree.insert("", END, values=("1023", "Padaria Estrela", "Impressora Térmica", "Concluídas", "R$ 150,00"))
    
    def abrir_popup_os(self):
        AddOSPopup(self, on_confirm=self.carregar_dados)

    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Busca do Banco (Query: id, cliente, equip, defeito, data, status, valor, prioridade)
        lista_os = OSModel.buscar_todos()
        
        for os in lista_os:
            valor_fmt = f"R$ {os[6]:.2f}"
            
            # Formatando a data (pegando apenas dia/mês/ano se vier com hora)
            data_crua = os[4]
            data_fmt = data_crua.split()[0] if data_crua else ""
            
            # CORREÇÃO: Mapeando os índices corretos
            # os[7] é a Prioridade (conforme sua Query no OSModel)
            self.tree.insert("", END, values=(os[0], os[1], os[2], os[7], data_fmt, os[5], valor_fmt))
    
    def ao_clicar_duplo(self, event):
        """Pega o item selecionado e abre edição"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        # O ID da OS é o primeiro valor da lista (values[0])
        id_os = item['values'][0]
        
        # Abre o Popup de Edição
        EditOSPopup(self, on_confirm=self.carregar_dados, id_os=id_os)
    
    def imprimir_selecionada(self):
        selection = self.tree.selection()
        if not selection:
            Messagebox.show_warning("Selecione uma OS na tabela para imprimir.")
            return
        
        # Pega o ID da linha selecionada
        item = self.tree.item(selection[0])
        id_os = item['values'][0]
        
        # Busca os dados COMPLETOS no banco (igual fazemos na edição)
        dados_completos = OSModel.buscar_por_id(id_os)
        
        if dados_completos:
            PDFManager.gerar_os(dados_completos)
        else:
            Messagebox.show_error("Erro ao buscar dados da OS.")
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class DashboardScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.pack(fill=BOTH, expand=YES)

        # Cabeçalho
        ttk.Label(self, text='Visão Geral', font=('Calibri', 24, 'bold'), bootstyle='primary').pack(anchor=W, pady=(0,20))
        
        # --- CARDS DE KPI ---
        cards_frame = ttk.Frame(self)
        cards_frame.pack(fill=X, pady=10)

        self.criar_card(cards_frame, 'Faturamento Hoje', 'R$ 1.250,00', 'success', 0)
        self.criar_card(cards_frame, 'OS Pendentes', '8', 'warning', 1)
        self.criar_card(cards_frame, 'Contas a Pagar', 'R$ 450,00', 'danger', 2)
        self.criar_card(cards_frame, 'Novos Clientes', '3', 'info', 3)
        
        # --- TABELA DE MOVIMENTAÇÃO RECENTE ---
        ttk.Label(self, text='Atividades Recentes', font=('Calibri', 14, 'bold'), bootstyle="secondary").pack(anchor=W, pady=(30,10))
        
        # Treeview (Tabela Nativa)
        colunas = ['Data', 'Descrição', 'Tipo', 'Valor']
        self.tree = ttk.Treeview(self, columns=colunas, show='headings', height=8, bootstyle='info')

        # Configurações Individuais de Coluna (Para corrigir o espaçamento)
        # Anchor W = Alinhado a Esquerda | Anchor CENTER = Centralizado
        self.tree.column('Data', width=100, anchor=CENTER)
        self.tree.column('Descrição', width=400, anchor=W) 
        self.tree.column('Tipo', width=100, anchor=CENTER)
        self.tree.column('Valor', width=100, anchor=E) # Valor alinhado a direita (E)

        # Cabeçalhos Corrigidos
        for col in colunas:
            self.tree.heading(col, text=col) # <--- AQUI ESTAVA O ERRO
        
        self.tree.pack(fill=X) # fill=X usa apenas a altura necessária (não expande vazio)

        # Dados Fakes
        dados_teste = [
            ("15/01/2026", "Abertura de Caixa - Turno Manhã", "Sistema", "-"),
            ("15/01/2026", "Venda Balcão #100 - Cliente João", "Entrada", "R$ 150,00"),
            ("15/01/2026", "Pagamento Fornecedor Energia", "Saída", "R$ 300,00"),
            ("15/01/2026", "Serviço OS #55 - Formatação", "Entrada", "R$ 120,00"),
        ]

        for item in dados_teste:
            self.tree.insert('', END, values=item)
    
    def criar_card(self, parent, titulo, valor, cor, col):
        card = ttk.Frame(parent, bootstyle=cor, padding=15)
        card.pack(side=LEFT, fill=BOTH, expand=YES, padx=10)

        ttk.Label(card, text=titulo, font=("Calibri", 12), bootstyle=f"inverse-{cor}").pack(anchor=W)
        ttk.Label(card, text=valor, font=("Calibri", 22, "bold"), bootstyle=f"inverse-{cor}").pack(anchor=W)
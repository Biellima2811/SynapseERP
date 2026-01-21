import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from core.finance_model import FinanceModel
from gui.popups import AddExpensePopup

class FinanceScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.pack(fill=BOTH, expand=YES)

        # Cabeçalho
        topo = ttk.Frame(self)
        topo.pack(fill=X, pady=(0, 20))
        ttk.Label(topo, text='Controle Financeiro & Caixa', font=('Calibri', 24, 'bold'), bootstyle='primary').pack(side=LEFT)
        ttk.Button(topo, text='- Lançar Despesa', bootstyle='danger', command=self.abrir_popup_despesa).pack(side=RIGHT)

        # --- CARDS DE BALANÇO ---
        cards_frame = ttk.Frame(self)
        cards_frame.pack(fill=X, pady=10)
        
        self.card_receita = self.criar_card(cards_frame, "Receitas (OS Concluídas)", "R$ 0,00", "success")
        self.card_despesa = self.criar_card(cards_frame, "Despesas Totais", "R$ 0,00", "danger")
        self.card_saldo = self.criar_card(cards_frame, "Lucro Líquido", "R$ 0,00", "info")

        # --- TABELA DE DESPESAS (CORREÇÃO AQUI) ---
        ttk.Label(self, text="Histórico de Saídas / Despesas", font=("Calibri", 14, "bold"), bootstyle="secondary").pack(anchor=W, pady=(30, 10))

        # 1. IDs das colunas (SEM ACENTO, SEM ERRO DE DIGITAÇÃO)
        colunas = ["id", "data", "descricao", "categoria", "valor"]
        
        self.tree = ttk.Treeview(self, columns=colunas, show='headings', bootstyle='danger', height=8)
        
        # 2. Configuração das Colunas (Usando os MESMOS IDs de cima)
        self.tree.column('id', width=50, anchor=CENTER)
        self.tree.column('data', width=100, anchor=CENTER)
        
        # AQUI ESTAVA O ERRO: 'decrição' vs 'descricao'
        self.tree.column('descricao', width=300, anchor=W) 
        
        self.tree.column('categoria', width=150, anchor=CENTER)
        self.tree.column('valor', width=100, anchor=E)
        
        # 3. Cabeçalhos (Texto visível para o usuário - Pode ter acento)
        self.tree.heading('id', text="ID")
        self.tree.heading('data', text="Data")
        self.tree.heading('descricao', text="Descrição")
        self.tree.heading('categoria', text="Categoria")
        self.tree.heading('valor', text="Valor (R$)")
        
        self.tree.pack(fill=BOTH, expand=YES)
        
        # Botão Excluir
        ttk.Button(self, text="Estornar / Excluir Lançamento", bootstyle="link-danger", command=self.excluir_lancamento).pack(anchor=E, pady=5)

        self.carregar_dados()

    def criar_card(self, parent, titulo, valor, cor):
        frame = ttk.Frame(parent, bootstyle=cor, padding=15)
        frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)
        
        lbl_titulo = ttk.Label(frame, text=titulo, font=("Calibri", 12), bootstyle=f"inverse-{cor}")
        lbl_titulo.pack(anchor=W)
        
        lbl_valor = ttk.Label(frame, text=valor, font=("Calibri", 22, "bold"), bootstyle=f"inverse-{cor}")
        lbl_valor.pack(anchor=W)
        
        return lbl_valor

    def carregar_dados(self):
        # 1. Atualiza Cards
        # (Não esqueça dos parênteses aqui também, se tiver faltando)
        rec, desp, saldo = FinanceModel.get_balanco_geral() 
        
        self.card_receita.config(text=f"R$ {rec:,.2f}")
        self.card_despesa.config(text=f"R$ {desp:,.2f}")
        self.card_saldo.config(text=f"R$ {saldo:,.2f}")
        
        # 2. Atualiza Tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        despesas = FinanceModel.buscar_despesas()
        
        for d in despesas:
            # d = (id, data, desc, cat, valor)
            valor_fmt = f"R$ {d[4]:,.2f}"
            data_fmt = d[1]
            try:
                partes = d[1].split('-')
                data_fmt = f"{partes[2]}/{partes[1]}/{partes[0]}"
            except: pass

            self.tree.insert("", END, values=(d[0], data_fmt, d[2], d[3], valor_fmt))
    def abrir_popup_despesa(self):
        AddExpensePopup(self, on_confirm=self.carregar_dados)

    def excluir_lancamento(self):
        sel = self.tree.selection()
        if not sel: return
        id_item = self.tree.item(sel[0])['values'][0]
        
        if Messagebox.show_question("Tem certeza que deseja apagar este registro?", "Confirmar Exclusão") == "Yes":
            FinanceModel.excluir_despesa(id_item)
            self.carregar_dados()
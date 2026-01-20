import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from core.user_model import UserModel
from gui.popups import AddUserPopup

class UsersScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.pack(fill=BOTH, expand=YES)

        # Cabeçalho
        topo = ttk.Frame(self)
        topo.pack(fill=X, pady=(0,20))
        
        ttk.Label(topo, text='Gestão de Usuários e Permissões', font=('Calibri', 24, 'bold'), bootstyle='primary').pack(side=LEFT)
        ttk.Button(topo, text='+ Novo Usuário', bootstyle='success', command=self.abrir_popup_novo).pack(side=RIGHT)

        # Tabela
        # ATENÇÃO: Uniformizei para 'Nível' COM acento em tudo para evitar confusão
        colunas = ['ID', 'Usuário', 'Nível de Acesso', 'Status']
        self.tree = ttk.Treeview(self, columns=colunas, show='headings', bootstyle='info')

        self.tree.column('ID', width=50, anchor=CENTER)
        self.tree.column('Usuário', width=200, anchor=W) # Mudei para W (esquerda) fica mais bonito texto
        self.tree.column('Nível de Acesso', width=150, anchor=CENTER)
        self.tree.column('Status', width=100, anchor=CENTER)

        for col in colunas: 
            self.tree.heading(col, text=col)

        self.tree.pack(fill=BOTH, expand=YES) # Faltava o pack da treeview para ela aparecer direito

        # Botões de Ação
        btn_frame = ttk.Frame(self, padding=(0,10))
        btn_frame.pack(fill=X)

        ttk.Button(btn_frame, text="✏️ Editar Senha/Nível", bootstyle="warning", command=self.editar_usuario).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Excluir Usuário", bootstyle="danger", command=self.excluir_usuario).pack(side=LEFT, padx=5)

        self.carregar_dados()
    
    def carregar_dados(self):
        for item  in self.tree.get_children():
            self.tree.delete(item)
        
        usuarios = UserModel.buscar_todos()
        for user in usuarios:
            # user = (id, usuario, nivel, ativo)
            status = 'Ativo' if user[3] else 'Inativo'
            # CORREÇÃO CRÍTICA: Adicionado 'END' antes dos values
            self.tree.insert('', END, values=(user[0], user[1], user[2].upper(), status))
    
    def abrir_popup_novo(self):
        AddUserPopup(self, on_confirm=self.carregar_dados)
    
    def editar_usuario(self):
        sel = self.tree.selection()
        if not sel:
            Messagebox.show_warning('Selecione um usuário para editar')
            return
        item = self.tree.item(sel[0])['values'] # (id, user, nivel, status)
        
        # Reutiliza o popup de adicionar, mas passando dados (Modo Edição)
        AddUserPopup(self, on_confirm=self.carregar_dados, dados_edicao=item)

    def excluir_usuario(self):
        sel = self.tree.selection()
        if not sel: return
        id_user = self.tree.item(sel[0])['values'][0]

        if Messagebox.show_question(f'Tem certeza que deseja excluir o usuário #{id_user}?', 'Confirmação') == 'Yes': # O padrão do ttkbootstrap retorna 'Yes', não 'SIM'
            if UserModel.excluir(id_user):
                Messagebox.show_info('Usuário excluído com sucesso!')
                self.carregar_dados()
            else:
                Messagebox.show_error('Não foi possível excluir! (Talvez seja o último admin)')
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os
import webbrowser
from datetime import datetime

class PDFManager:
    
    @staticmethod
    def gerar_os(dados_os):
        """
        Gera um PDF elegante da Ordem de Serviço
        dados_os: Tupla ou Objeto com (id, cliente, equip, defeito, obs, tecnico, status, valor, data, laudo, etc...)
        """
        # Garante a pasta 'docs'
        if not os.path.exists("docs"):
            os.makedirs("docs")
            
        id_os = dados_os[0]
        nome_arquivo = f"docs/OS_{id_os}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        c = canvas.Canvas(nome_arquivo, pagesize=A4)
        largura, altura = A4
        
        # --- CABEÇALHO ---
        # Fundo do cabeçalho
        c.setFillColor(colors.HexColor("#2C3E50")) # Azul escuro do tema
        c.rect(0, altura - 100, largura, 100, fill=True, stroke=False)
        
        # Logo (Tenta carregar a do Synapse ou Guardião)
        logo_path = "assets/SynapseERP.png"
        if not os.path.exists(logo_path):
            logo_path = "assets/logo_guardiao.png"
            
        if os.path.exists(logo_path):
            try:
                # Desenha a logo (x, y, w, h)
                c.drawImage(logo_path, 20, altura - 90, width=70, height=70, mask='auto')
            except: pass

        # Títulos
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(110, altura - 50, "Synapse ERP")
        c.setFont("Helvetica", 12)
        c.drawString(110, altura - 70, "Gestão Inteligente & Assistência Técnica")
        
        # Número da OS (Destaque)
        c.setFont("Helvetica-Bold", 20)
        c.drawRightString(largura - 20, altura - 50, f"OS Nº {id_os:04d}")
        c.setFont("Helvetica", 10)
        c.drawRightString(largura - 20, altura - 70, f"Emissão: {datetime.now().strftime('%d/%m/%Y')}")

        # --- CORPO DO DOCUMENTO ---
        y = altura - 140
        c.setFillColor(colors.black)
        
        # Função auxiliar para desenhar linhas de dados
        def desenhar_linha(titulo, valor, pos_y):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(40, pos_y, f"{titulo}:")
            c.setFont("Helvetica", 10)
            # Limita tamanho do texto para não estourar a margem
            valor = str(valor)
            if len(valor) > 90: valor = valor[:90] + "..."
            c.drawString(150, pos_y, valor)
            # Linha cinza embaixo
            c.setStrokeColor(colors.lightgrey)
            c.line(40, pos_y - 5, largura - 40, pos_y - 5)
            return pos_y - 25

        # Dados do Cliente
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#2980B9"))
        c.drawString(40, y, "DADOS DO CLIENTE")
        y -= 25
        c.setFillColor(colors.black)
        
        y = desenhar_linha("Cliente", dados_os[2], y) # nome (indice 2 na busca_por_id)
        # Buscaria telefone/cpf se fizesse join, por enquanto vamos com o que tem na OS
        
        y -= 10
        
        # Dados do Equipamento
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#2980B9"))
        c.drawString(40, y, "DETALHES DO SERVIÇO")
        y -= 25
        c.setFillColor(colors.black)
        
        y = desenhar_linha("Equipamento", dados_os[3], y)
        y = desenhar_linha("Defeito Relatado", dados_os[4], y)
        y = desenhar_linha("Prioridade", dados_os[7], y)
        y = desenhar_linha("Técnico", dados_os[6], y)
        y = desenhar_linha("Status Atual", dados_os[8], y)
        
        # Laudo Técnico (Área maior)
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "Laudo Técnico / Serviços Executados:")
        y -= 20
        c.setFont("Helvetica", 10)
        
        laudo = dados_os[11] if dados_os[11] else "Ainda não preenchido."
        # Quebra de texto simples
        text_object = c.beginText(40, y)
        text_object.setFont("Helvetica", 10)
        # Wrap manual simples (em sistema real usaríamos Paragraph do platypus)
        words = laudo.split()
        line = ""
        for word in words:
            if c.stringWidth(line + word) < 500:
                line += word + " "
            else:
                text_object.textLine(line)
                line = word + " "
                y -= 12
        text_object.textLine(line)
        c.drawText(text_object)
        
        y -= 40
        
        # Valores
        c.setFillColor(colors.HexColor("#E74C3C")) # Vermelho para destaque financeiro
        c.setFont("Helvetica-Bold", 16)
        c.drawRightString(largura - 40, y, f"Total Estimado: R$ {dados_os[9]:.2f}")
        
        # --- RODAPÉ (Assinaturas) ---
        y_foot = 100
        c.setStrokeColor(colors.black)
        c.line(50, y_foot, 250, y_foot)
        c.line(340, y_foot, 540, y_foot)
        
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.black)
        c.drawCentredString(150, y_foot - 15, "Assinatura do Técnico")
        c.drawCentredString(440, y_foot - 15, "Assinatura do Cliente")
        
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(largura/2, 30, "Documento gerado eletronicamente por SynapseERP")
        
        c.save()
        
        # Abre o PDF automaticamente
        try:
            webbrowser.open(os.path.abspath(nome_arquivo))
        except:
            print("PDF gerado mas não foi possível abrir automaticamente.")
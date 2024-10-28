import os
from PyPDF2 import PdfReader, PdfWriter
from tkinter import Tk, filedialog, messagebox

def salvar_paginas(pdf_reader, start_page, end_page, output_path, nome_arquivo):

    output_pdf = PdfWriter()
    for i in range(start_page, end_page):
        output_pdf.add_page(pdf_reader.pages[i])
    try:
        with open(f"{output_path}/{nome_arquivo}.pdf", "wb") as output_file:
            output_pdf.write(output_file)
        print(f"Arquivo salvo: {nome_arquivo}.pdf")
    except Exception as e:
        print(f"Erro ao salvar {nome_arquivo}: {e}")

def extrair_titulo_pagina(pagina):
 
    texto = pagina.extract_text() or ""
    linhas = texto.split("\n")
    
    if len(linhas) > 0:
        titulo = linhas[0].strip()
        if len(titulo) > 0:
            return titulo
    return None

def identificar_contrato(pagina):
   
    texto = pagina.extract_text() or ""
    return "CONTRATO DE PRESTAÇÃO DE SERVIÇOS" in texto.upper()

def dividir_pdf_por_partes(pdf_path, output_path):
    pdf_reader = PdfReader(pdf_path)
    total_paginas = len(pdf_reader.pages)
    
    pagina_atual = 0
    contrato_contador = 1
    doc_contador = 1

    while pagina_atual < total_paginas:
        if identificar_contrato(pdf_reader.pages[pagina_atual]):
    
            salvar_paginas(pdf_reader, pagina_atual, min(pagina_atual + 3, total_paginas), output_path, f"Contrato_{contrato_contador}")
            contrato_contador += 1
            pagina_atual += 3  
        else:
           
            titulo = extrair_titulo_pagina(pdf_reader.pages[pagina_atual])
            if titulo:
                nome_arquivo = titulo.replace(" ", "_").replace("/", "-").replace("\\", "-")
            else:
                nome_arquivo = f"Documento_{doc_contador}"
                doc_contador += 1
            
            salvar_paginas(pdf_reader, pagina_atual, pagina_atual + 1, output_path, nome_arquivo)
            pagina_atual += 1

def executar_processamento(pdf_path, output_path):
    dividir_pdf_por_partes(pdf_path, output_path)
  
    messagebox.showinfo("Concluído", "O processamento do PDF foi concluído com sucesso!")

def escolher_arquivos():
    root = Tk()
    root.withdraw() 

    pdf_path = filedialog.askopenfilename(title="Selecione o PDF", filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        print("Nenhum arquivo PDF selecionado.")
        return

    output_path = filedialog.askdirectory(title="Selecione o diretório de saída")
    if not output_path:
        print("Nenhum diretório de saída selecionado.")
        return

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    executar_processamento(pdf_path, output_path)

escolher_arquivos()

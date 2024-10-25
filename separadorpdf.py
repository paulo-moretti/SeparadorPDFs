import os
from PyPDF2 import PdfReader, PdfWriter
from tkinter import Tk, filedialog

def separar_pdf(arquivo_pdf, pasta_saida):
    leitor = PdfReader(arquivo_pdf)
    total_paginas = len(leitor.pages)

    for i in range(total_paginas):
        escritor = PdfWriter()
        escritor.add_page(leitor.pages[i])
        nome_arquivo = f"pagina_{i + 1}.pdf"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        
        with open(caminho_completo, "wb") as novo_pdf:
            escritor.write(novo_pdf)

        print(f"Página {i + 1} salva em: {caminho_completo}")

    print(f"Todas as {total_paginas} páginas foram separadas e salvas na pasta: {pasta_saida}")

def escolher_arquivo_e_pasta():
    root = Tk()
    root.withdraw()

    arquivo_pdf = filedialog.askopenfilename(
        title="Selecione o arquivo PDF para separar",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )

    if not arquivo_pdf:
        print("Nenhum arquivo selecionado.")
        return

    pasta_saida = filedialog.askdirectory(
        title="Selecione a pasta onde deseja salvar as páginas separadas"
    )

    if not pasta_saida:
        print("Nenhuma pasta selecionada.")
        return

    separar_pdf(arquivo_pdf, pasta_saida)

escolher_arquivo_e_pasta()

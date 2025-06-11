import tkinter as tk
from tkinter import filedialog, messagebox
import os
from tratarTXT import main

def selecionar_arquivo_excel():
    caminho = filedialog.askopenfilename(
        title="Selecione a planilha modelo Excel",
        filetypes=[("Arquivos Excel", "*.xlsx")]
    )
    if caminho:
        entry_excel.delete(0, tk.END)
        entry_excel.insert(0, caminho)

def selecionar_arquivo_pdf():
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo PDF de comprovantes",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if caminho:
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, caminho)

def selecionar_pasta_cliente():
    caminho = filedialog.askdirectory(
        title="Selecione a pasta do cliente"
    )
    if caminho:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, caminho)

def executar():
    excel = entry_excel.get()
    pdf = entry_pdf.get()
    pasta = entry_pasta.get()
    cnpj = entry_cnpj.get().strip()

    if not (excel and pdf and pasta and cnpj):
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    try:
        saida = main(excel, pdf, pasta, cnpj)
        messagebox.showinfo("Sucesso", f"Processamento concluído!\nArquivo salvo em:\n{saida}")
    except Exception as e:
        messagebox.showerror("Erro na execução", str(e))

# Interface
root = tk.Tk()
root.title("Processador Sistema S - e-CAC")

tk.Label(root, text="Planilha Modelo Excel:").grid(row=0, column=0, sticky="e")
entry_excel = tk.Entry(root, width=50)
entry_excel.grid(row=0, column=1)
tk.Button(root, text="Selecionar", command=selecionar_arquivo_excel).grid(row=0, column=2)

tk.Label(root, text="Arquivo PDF Comprovantes:").grid(row=1, column=0, sticky="e")
entry_pdf = tk.Entry(root, width=50)
entry_pdf.grid(row=1, column=1)
tk.Button(root, text="Selecionar", command=selecionar_arquivo_pdf).grid(row=1, column=2)

tk.Label(root, text="Pasta do Cliente:").grid(row=2, column=0, sticky="e")
entry_pasta = tk.Entry(root, width=50)
entry_pasta.grid(row=2, column=1)
tk.Button(root, text="Selecionar", command=selecionar_pasta_cliente).grid(row=2, column=2)

tk.Label(root, text="CNPJ do Cliente:").grid(row=3, column=0, sticky="e")
entry_cnpj = tk.Entry(root, width=30)
entry_cnpj.grid(row=3, column=1, sticky="w")

tk.Button(root, text="Executar", command=executar, bg="#4CAF50", fg="white", width=20).grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
from tkinter import *
from tkinter import ttk, filedialog, simpledialog
root = Tk()
import PyPDF2
from tkinter import messagebox

def remover_protecao(pdf_path, senha):
    try:
        # Abrir o arquivo PDF original
        with open(pdf_path, "rb") as arquivo_pdf:
            leitor = PyPDF2.PdfReader(arquivo_pdf)
            # Verificar se o PDF está criptografado e tentar descriptografar
            if leitor.is_encrypted:
                leitor.decrypt(senha)
            # Criar um novo PDF sem proteção
            output = PyPDF2.PdfWriter()
            for pagina in leitor.pages:
                output.add_page(pagina)
            # Definir o caminho do novo PDF
            pdf_desprotegido_path = pdf_path.replace(".pdf", "_desprotegido.pdf")
            # Salvar o novo PDF
            with open(pdf_desprotegido_path, "wb") as novo_pdf:
                output.write(novo_pdf)
            
            return pdf_desprotegido_path
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao remover proteção do PDF: {str(e)}")
        return None

def upload():
    archive_pdf = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
    if archive_pdf:
        password = simpledialog.askstring("Senha do PDF", "Digite a senha do PDF (deixe em branco se não houver):")
        if password is None:  # Usuário cancelou a entrada de senha
            return
        caminho_pdf = remover_protecao(archive_pdf, password)
        if caminho_pdf:
            caminho_arquivo_var.set(caminho_pdf)

root.title("Fatura")
frm = ttk.Frame(root, padding=30)
frm.grid()
caminho_arquivo_var = StringVar()
# ttk.Label(frm, text="Escolha um arquivo PDF:").grid(column=0, row=0)
ttk.Entry(frm, textvariable=caminho_arquivo_var, width=10).grid(column=1, row=0)
ttk.Button(frm, text="Upload", command=upload).grid(column=0, row=0)
ttk.Button(frm, text="Visualizar", command=root.destroy).grid(column=0, row=1)
ttk.Button(frm, text="Salvar", command=root.destroy).grid(column=1, row=1)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=1)
root.mainloop()
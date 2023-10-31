import tkinter as tk
import tkinter.filedialog as filedialog
import sqlite3
from tkinter import ttk
from tkinter import messagebox

# Parte I: Interface para submissão de dados do desenvolvedor

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_cidade.delete(0, tk.END)
    entry_estado.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    text_experiencia.delete("1.0", tk.END)
    text_empregabilidade.delete("1.0", tk.END)
    entry_linkedin.delete(0, tk.END)
    entry_curriculo.delete(0, tk.END)

def salvar_dados():
    nome = entry_nome.get()
    idade = entry_idade.get()
    cidade = entry_cidade.get()
    estado = entry_estado.get()
    telefone = entry_telefone.get()
    email = entry_email.get()
    experiencia = text_experiencia.get("1.0", tk.END)
    empregabilidade = text_empregabilidade.get("1.0", tk.END)
    linkedin = entry_linkedin.get()
    curriculo_path = entry_curriculo.get()

# Obter o caminho do arquivo de currículo
    curriculo_path = entry_curriculo.get()

    if not curriculo_path:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo de currículo.")
        return

    try:
        with open(curriculo_path, 'rb') as file:
            curriculo = file.read()
    except FileNotFoundError:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo de currículo válido.")
        return

    # Conectar ao banco de dados e inserir os dados
    conn = sqlite3.connect("dados_dev.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO desenvolvedores (nome, idade, cidade, estado, telefone, email, experiencia, empregabilidade, linkedin, curriculo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (nome, idade, cidade, estado, telefone, email, experiencia, empregabilidade, linkedin, curriculo))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Dados do desenvolvedor foram salvos com sucesso!")
    limpar_campos()  # Chama a função para limpar os campos após salvar

# Função para selecionar o currículo
def selecionar_curriculo():
    curriculo_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
    entry_curriculo.delete(0, tk.END)
    entry_curriculo.insert(0, curriculo_path)

# Parte I: Interface para submissão de dados do desenvolvedor
frame_dev = ttk.LabelFrame(root, text="Dados do Desenvolvedor")
frame_dev.grid(row=0, column=0, padx=10, pady=10)

# ... Definição de rótulos e entradas ...

btn_salvar = tk.Button(frame_dev, text="Salvar", command=salvar_dados)
btn_salvar.grid(row=10, columnspan=3)

# Parte II: Interface para o recrutador

def filtrar_candidatos():
    cidade = entry_cidade_filtro.get()
    estado = entry_estado_filtro.get()
    salario = entry_salario_filtro.get()
    area_trabalho = entry_area_trabalho_filtro.get()

    # Conectar ao banco de dados e executar a consulta
    conn = sqlite3.connect("dados_dev.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM desenvolvedores WHERE cidade=? AND estado=? AND expectativa_salarial<=? AND area_trabalho=?",
                   (cidade, estado, salario, area_trabalho))
    candidatos = cursor.fetchall()
    conn.close()

    # Exibir os resultados em uma nova janela
    janela_resultado = tk.Toplevel()
    janela_resultado.title("Candidatos")

    tree = ttk.Treeview(janela_resultado, columns=("Nome", "Email", "Telefone", "Status"))
    tree.heading("#1", text="Nome")
    tree.heading("#2", text="Email")
    tree.heading("#3", text="Telefone")
    tree.heading("#4", text="Status")

    for candidato in candidatos:
        tree.insert("", "end", values=(candidato[1], candidato[6], candidato[5], "Em Espera"))

    tree.pack()

# Criação da janela principal
root = tk.Tk()
root.title("Sistema de Recrutamento")

# Parte I: Interface para submissão de dados do desenvolvedor
frame_dev = ttk.LabelFrame(root, text="Dados do Desenvolvedor")
frame_dev.grid(row=0, column=0, padx=10, pady=10)

label_nome = tk.Label(frame_dev, text="Nome:")
label_nome.grid(row=0, column=0)
entry_nome = tk.Entry(frame_dev)
entry_nome.grid(row=0, column=1)

label_idade = tk.Label(frame_dev, text="Idade:")
label_idade.grid(row=1, column=0)
entry_idade = tk.Entry(frame_dev)
entry_idade.grid(row=1, column=1)

label_cidade = tk.Label(frame_dev, text="Cidade:")
label_cidade.grid(row=2, column=0)
entry_cidade = tk.Entry(frame_dev)
entry_cidade.grid(row=2, column=1)

label_estado = tk.Label(frame_dev, text="Estado:")
label_estado.grid(row=3, column=0)
entry_estado = tk.Entry(frame_dev)
entry_estado.grid(row=3, column=1)

label_telefone = tk.Label(frame_dev, text="Telefone:")
label_telefone.grid(row=4, column=0)
entry_telefone = tk.Entry(frame_dev)
entry_telefone.grid(row=4, column=1)

label_email = tk.Label(frame_dev, text="E-mail:")
label_email.grid(row=5, column=0)
entry_email = tk.Entry(frame_dev)
entry_email.grid(row=5, column=1)

label_experiencia = tk.Label(frame_dev, text="Experiência:")
label_experiencia.grid(row=6, column=0)
text_experiencia = tk.Text(frame_dev, height=5, width=30)
text_experiencia.grid(row=6, column=1)

label_empregabilidade = tk.Label(frame_dev, text="Empregabilidade:")
label_empregabilidade.grid(row=7, column=0)
text_empregabilidade = tk.Text(frame_dev, height=5, width=30)
text_empregabilidade.grid(row=7, column=1)

label_linkedin = tk.Label(frame_dev, text="LinkedIn:")
label_linkedin.grid(row=8, column=0)
entry_linkedin = tk.Entry(frame_dev)
entry_linkedin.grid(row=8, column=1)

label_curriculo = tk.Label(frame_dev, text="Currículo:")
label_curriculo.grid(row=9, column=0)
entry_curriculo = tk.Entry(frame_dev)
entry_curriculo.grid(row=9, column=1)

btn_selecionar_curriculo = tk.Button(frame_dev, text="Selecionar Currículo", command=selecionar_curriculo)
btn_selecionar_curriculo.grid(row=9, column=2)

btn_salvar = tk.Button(frame_dev, text="Salvar", command=salvar_dados)
btn_salvar.grid(row=10, columnspan=3)

# Parte II: Interface para o recrutador
frame_rec = ttk.LabelFrame(root, text="Filtrar Candidatos")
frame_rec.grid(row=1, column=0, padx=10, pady=10)

label_cidade_filtro = tk.Label(frame_rec, text="Cidade:")
label_cidade_filtro.grid(row=0, column=0)
entry_cidade_filtro = tk.Entry(frame_rec)
entry_cidade_filtro.grid(row=0, column=1)

label_estado_filtro = tk.Label(frame_rec, text="Estado:")
label_estado_filtro.grid(row=1, column=0)
entry_estado_filtro = tk.Entry(frame_rec)
entry_estado_filtro.grid(row=1, column=1)

label_salario_filtro = tk.Label(frame_rec, text="Salário Máximo:")
label_salario_filtro.grid(row=2, column=0)
entry_salario_filtro = tk.Entry(frame_rec)
entry_salario_filtro.grid(row=2, column=1)

label_area_trabalho_filtro = tk.Label(frame_rec, text="Área de Trabalho:")
label_area_trabalho_filtro.grid(row=3, column=0)
entry_area_trabalho_filtro = tk.Entry(frame_rec)
entry_area_trabalho_filtro.grid(row=3, column=1)

btn_filtrar = tk.Button(frame_rec, text="Filtrar Candidatos", command=filtrar_candidatos)
btn_filtrar.grid(row=4, columnspan=2)

# Criação do banco de dados
conn = sqlite3.connect("dados_dev.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS desenvolvedores 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nome TEXT, idade INTEGER, cidade TEXT, estado TEXT, 
                 telefone TEXT, email TEXT, experiencia TEXT, empregabilidade TEXT, 
                 linkedin TEXT, curriculo TEXT)''')
conn.commit()
conn.close()

root.mainloop()
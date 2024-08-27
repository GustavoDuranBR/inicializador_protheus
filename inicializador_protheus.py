import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import webbrowser
from config import open_settings, paths

processes = []

def run_command(command, log_widget):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(process)
        log_widget.insert(tk.END, f"Executando: {command}\n")
        while process.poll() is None:
            root.update_idletasks()
        log_widget.insert(tk.END, f"Tarefa concluída: {command}\n")
    except Exception as e:
        log_widget.insert(tk.END, f"Erro: {str(e)}\n")
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
    finally:
        for button in buttons:
            button.config(state=tk.NORMAL)

def start_task(path_key):
    command = f'start "" "{paths[path_key]}"'
    for button in buttons:
        button.config(state=tk.DISABLED)
    log_box.insert(tk.END, f"Iniciando tarefa: {path_key}\n")
    threading.Thread(target=run_command, args=(command, log_box)).start()

def open_browser():
    for button in buttons:
        button.config(state=tk.DISABLED)
    log_box.insert(tk.END, "Abrindo navegador...\n")

    try:
        webbrowser.open("http://localhost:8089")
        log_box.insert(tk.END, "Navegador aberto com sucesso!\n")
    except Exception as e:
        log_box.insert(tk.END, f"Erro ao abrir o navegador: {str(e)}\n")
        messagebox.showerror("Erro", f"Ocorreu um erro ao abrir o navegador: {str(e)}")
    finally:
        for button in buttons:
            button.config(state=tk.NORMAL)

def terminate_processes():
    for process in processes:
        if process.poll() is None:
            process.terminate()

def quit_app():
    if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
        root.quit()
        root.destroy()

root = tk.Tk()
root.title("Inicializador Protheus")
root.iconbitmap("icon.ico")
root.geometry("700x500")
root.configure(bg='#333333')

# Estilo para tema dark
style = ttk.Style()
style.theme_use('default')
style.configure('TButton', background='#444444', foreground='#8bb7f7', font=('Arial', 10))
style.map('TButton', background=[('active', '#555555')])

label = tk.Label(root, text="Inicializador Protheus", bg='#333333', fg='#8bb7f7', font=('Arial', 16))
label.pack(pady=10)

# Frame para os botões, alinhado à esquerda
frame_buttons = tk.Frame(root, bg='#333333')
frame_buttons.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Caixa de diálogo
log_box = scrolledtext.ScrolledText(root, width=50, height=20, bg='#222222', 
                                    fg='#8bb7f7', state='normal')
log_box.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)

buttons = []

tasks = [
    ("Iniciar Dbaccess", "Dbaccess"),
    ("Iniciar Appserver", "Appserver"),
]

for text, path_key in tasks:
    button = tk.Button(frame_buttons, text=text, command=lambda key=path_key: start_task(key), 
                       width=25, bg='#444444', fg='#8bb7f7', relief='flat')
    button.pack(pady=5, anchor=tk.W)
    buttons.append(button)

browser_button = tk.Button(frame_buttons, text="Iniciar Protheus WEB", command=open_browser, 
                           width=25, bg='#444444', fg='#8bb7f7', relief='flat')
browser_button.pack(pady=5, anchor=tk.W)
buttons.append(browser_button)

tasks_rest = [
    ("Iniciar Smartclient", "Smartclient"),
    ("Atualizar RPO", "Baixar_RPO"),
]

for text, path_key in tasks_rest:
    button = tk.Button(frame_buttons, text=text, command=lambda key=path_key: start_task(key), 
                       width=25, bg='#444444', fg='#8bb7f7', relief='flat')
    button.pack(pady=5, anchor=tk.W)
    buttons.append(button)

settings_button = tk.Button(frame_buttons, text="Configurações", command=lambda: open_settings(root), 
                            width=25, bg='#444444', fg='#8bb7f7', relief='flat')
settings_button.pack(pady=5, anchor=tk.W)
buttons.append(settings_button)

exit_button = tk.Button(frame_buttons, text="Sair", command=quit_app, 
                        width=25, bg='#444444', fg='#8bb7f7', relief='flat')
exit_button.pack(pady=5, anchor=tk.W)
buttons.append(exit_button)

# Informações do desenvolvedor e versão, alinhadas à esquerda junto com os botões
dev_label = tk.Label(frame_buttons, text="Dev: Gustavo Duran", bg='#333333', fg='#8bb7f7')
dev_label.pack(pady=5, anchor=tk.W)

version_label = tk.Label(frame_buttons, text="Versão: 2.1", bg='#333333', fg='#8bb7f7')
version_label.pack(pady=5, anchor=tk.W)

root.protocol("WM_DELETE_WINDOW", quit_app)
root.mainloop()
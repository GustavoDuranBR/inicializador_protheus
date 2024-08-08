import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import webbrowser
from config import open_settings, paths
from tooltip import ToolTip

processes = []

def run_command(command, progress, label):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(process)
        while process.poll() is None:
            progress.step(10)
            root.update_idletasks()
        progress.step(100 - progress['value'])
        label.config(text="Tarefa concluída!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
    finally:
        for button in buttons:
            button.config(state=tk.NORMAL)

def start_task(path_key):
    command = f'start "" "{paths[path_key]}"'
    for button in buttons:
        button.config(state=tk.DISABLED)
    progress['value'] = 0
    label.config(text="Executando...")
    threading.Thread(target=run_command, args=(command, progress, label)).start()

def open_browser():
    for button in buttons:
        button.config(state=tk.DISABLED)
    progress['value'] = 0
    label.config(text="Abrindo navegador...")

    try:
        webbrowser.open("http://localhost:8089")
        label.config(text="Navegador aberto!")
    except Exception as e:
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

label = tk.Label(root, text="Inicializador Protheus")
label.pack(pady=10)

progress = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
progress.pack(pady=10)

buttons = []

tasks = [
    ("Iniciar Dbaccess", "Dbaccess"),
    ("Iniciar Appserver", "Appserver"),
]

for text, path_key in tasks:
    button = tk.Button(root, text=text, command=lambda key=path_key: start_task(key))
    button.pack(pady=5)
    buttons.append(button)

browser_button = tk.Button(root, text="Iniciar Protheus WEB", command=open_browser)
browser_button.pack(pady=5)
buttons.append(browser_button)

tasks_rest = [
    ("Iniciar Smartclient", "Smartclient"),
    ("Atualizar RPO", "Baixar_RPO"),
]

for text, path_key in tasks_rest:
    button = tk.Button(root, text=text, command=lambda key=path_key: start_task(key))
    button.pack(pady=5)
    buttons.append(button)

settings_button = tk.Button(root, text="Configurações", command=lambda: open_settings(root))
settings_button.pack(pady=5)
buttons.append(settings_button)

exit_button = tk.Button(root, text="Sair", command=quit_app)
exit_button.pack(pady=5)
buttons.append(exit_button)

label = tk.Label(root, text="Dev: Gustavo Duran")
label.pack(pady=1)
label = tk.Label(root, text="Versão: 1.0")
label.pack(pady=1)
root.protocol("WM_DELETE_WINDOW", quit_app)
root.mainloop()

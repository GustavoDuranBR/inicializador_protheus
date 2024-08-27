import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import webbrowser
from config import open_settings, paths
from atualizar_rpo import update_rpo

processes = []

def run_command(command, log_box, start_message):
    log_box.insert(tk.END, f"{start_message}\n")
    log_box.yview(tk.END)
    
    try:
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        log_box.insert(tk.END, f"Erro ao executar: {command}\n{e.stderr}\n")
        log_box.yview(tk.END)

def start_task(path_key):
    command = f'start "" "{paths[path_key]}"'
    log_box.insert(tk.END, f"Iniciando tarefa: {path_key}\n")
    threading.Thread(target=run_command, args=(command, log_box, path_key)).start()

def start_update_rpo():
    version = paths.get("Versao_RPO", "")
    if not version:
        messagebox.showerror("Erro", "A versão RPO não está definida. Por favor, configure nas Configurações.")
        return
    
    log_box.insert(tk.END, "Atualizando RPO...\n")
    threading.Thread(target=update_rpo, args=(version, log_box, root)).start()

def start_dbaccess_and_appserver():
    log_box.insert(tk.END, "Iniciando DbAccess e AppServer...\n")
    
    # Iniciar DbAccess
    dbaccess_command = f'start "" "{paths["Dbaccess"]}"'
    threading.Thread(target=run_command, args=(dbaccess_command, log_box, "Executando: DbAccess")).start()

    # Iniciar Appserver
    appserver_command = f'start "" "{paths["Appserver"]}"'
    threading.Thread(target=run_command, args=(appserver_command, log_box, "Executando: AppServer")).start()

def restart_dbaccess_and_appserver(log_box):
    log_box.insert(tk.END, "Reiniciando DbAccess e AppServer...\n")
    
    # Fechar DbAccess e AppServer
    dbaccess_close_command = "taskkill /F /IM dbaccess64.exe"
    appserver_close_command = "taskkill /F /IM appserver.exe"
    threading.Thread(target=run_command, args=(dbaccess_close_command, log_box, "Fechando: DbAccess")).start()
    threading.Thread(target=run_command, args=(appserver_close_command, log_box, "Fechando: AppServer")).start()
    
    # Reiniciar DbAccess
    dbaccess_command = f'start "" "{paths["Dbaccess"]}"'
    threading.Thread(target=run_command, args=(dbaccess_command, log_box, "Reiniciando: DbAccess")).start()

    # Reiniciar Appserver
    appserver_command = f'start "" "{paths["Appserver"]}"'
    threading.Thread(target=run_command, args=(appserver_command, log_box, "Reiniciando: AppServer")).start()


def close_all_processes():
    try:
        subprocess.run("taskkill /F /IM dbaccess64.exe", shell=True, check=True)
        subprocess.run("taskkill /F /IM appserver.exe", shell=True, check=True)
    except subprocess.CalledProcessError:
        pass  # Ignorar erros se os processos já estiverem fechados

def open_browser():
    log_box.insert(tk.END, "Abrindo navegador...\n")

    try:
        webbrowser.open("http://localhost:8089")
        log_box.insert(tk.END, "Navegador aberto com sucesso!\n")
    except Exception as e:
        log_box.insert(tk.END, f"Erro ao abrir o navegador: {str(e)}\n")
        messagebox.showerror("Erro", f"Ocorreu um erro ao abrir o navegador: {str(e)}")

def quit_app():
    if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
        close_all_processes()  # Fechar processos antes de sair
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

# Criando o botão para iniciar DbAccess e AppServer juntos
start_button = tk.Button(frame_buttons, text="Iniciar DbAccess e AppServer", 
                         command=start_dbaccess_and_appserver, 
                         width=25, bg='#444444', fg='#8bb7f7', relief='flat')
start_button.pack(pady=5, anchor=tk.W)
buttons.append(start_button)

# Botão para reiniciar DbAccess e AppServer
restart_button = tk.Button(frame_buttons, text="Reiniciar DbAccess e AppServer", 
                         command=lambda: restart_dbaccess_and_appserver(log_box), 
                         width=25, bg='#444444', fg='#8bb7f7', relief='flat')
restart_button.pack(pady=5, anchor=tk.W)
buttons.append(restart_button)

# Botão para iniciar Protheus Web
browser_button = tk.Button(frame_buttons, text="Iniciar Protheus WEB", command=open_browser, 
                           width=25, bg='#444444', fg='#8bb7f7', relief='flat')
browser_button.pack(pady=5, anchor=tk.W)
buttons.append(browser_button)

# Botão para iniciar SmartClient e atualizar RPO
tasks_rest = [
    ("Iniciar Smartclient", "Smartclient"),
    ("Atualizar RPO", start_update_rpo),  
]

for text, action in tasks_rest:
    button = tk.Button(frame_buttons, text=text, command=action if callable(action) else lambda key=action: start_task(key), 
                       width=25, bg='#444444', fg='#8bb7f7', relief='flat')
    button.pack(pady=5, anchor=tk.W)
    buttons.append(button)

# Botão para abrir configurações
settings_button = tk.Button(frame_buttons, text="Configurações", command=lambda: open_settings(root), 
                            width=25, bg='#444444', fg='#8bb7f7', relief='flat')
settings_button.pack(pady=5, anchor=tk.W)
buttons.append(settings_button)

# Botão para sair do aplicativo
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

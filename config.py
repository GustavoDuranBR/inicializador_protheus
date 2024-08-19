import os
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import json
from tooltip import ToolTip

# Carrega os caminhos de paths.json, ou inicializa com valores vazios se não existir
if os.path.exists("paths.json"):
    with open("paths.json", "r") as file:
        paths = json.load(file)
else:
    paths = {
        "Dbaccess": "",
        "Appserver": "",
        "Smartclient": "",
        "Baixar_RPO": ""
    }

def remove_quotes(path):
    """Remove quotes from the given path."""
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    return path

def save_paths():
    """Save paths to the paths.json file."""
    with open("paths.json", "w") as file:
        json.dump(paths, file, indent=4)
    save_log()

def save_log():
    """Save paths to a log file."""
    with open("config_log.txt", "w") as log_file:
        for key, path in paths.items():
            log_file.write(f"{key}: {path}\n")

def open_settings(parent):
    settings_window = tk.Toplevel(parent)
    settings_window.title("Configurações")
    settings_window.iconbitmap("icon.ico")
    settings_window.configure(bg='#333333')  # Background da janela de configurações

    def save_path(path_key, is_directory=False):
        if is_directory:
            path = filedialog.askdirectory()
        else:
            path = filedialog.askopenfilename(filetypes=(("Link Files", "*.lnk"), ("All Files", "*.*")))
        if path:
            paths[path_key] = remove_quotes(path)
            save_paths()
            path_vars[path_key].set(paths[path_key])

    # Inicializa path_vars com valores do dicionário paths
    path_vars = {key: tk.StringVar(value=paths.get(key, "")) for key in paths}

    for i, (label_text, path_key) in enumerate(paths.items()):
        # Label com texto e fundo da janela
        label = tk.Label(settings_window, text=label_text, bg='#333333', fg='white')
        label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

        # Entry para exibir o caminho, com fundo branco e texto preto
        entry = tk.Entry(settings_window, textvariable=path_vars[label_text], width=50, state='readonly', bg='white', fg='black')
        entry.grid(row=i, column=1, padx=5, pady=5)
        ToolTip(entry, f"Defina o caminho para {label_text.lower()}")

        # Botão para procurar o caminho, com fundo cinza escuro e texto branco
        browse_button = tk.Button(settings_window, text="Procurar", command=lambda key=label_text: save_path(key), bg='#444444', fg='white')
        browse_button.grid(row=i, column=2, padx=5, pady=5)

    def copy_file():
        src = filedialog.askopenfilename(title="Selecione o arquivo appserver.ini", filetypes=(("INI files", "*.ini"), ("All files", "*.*")))
        if src:
            dst = filedialog.askdirectory(title="Selecione o diretório de destino")
            if dst:
                shutil.copy(src, dst)
                tk.messagebox.showinfo("Sucesso", f"Arquivo copiado para {dst}")

    copy_button = tk.Button(settings_window, text="Copiar appserver.ini", command=copy_file, bg='#444444', fg='white')
    copy_button.grid(row=len(paths), column=0, columnspan=3, pady=10)

    def save_and_close():
        save_paths()
        settings_window.destroy()

    save_button = tk.Button(settings_window, text="Salvar", command=save_and_close, bg='#444444', fg='white')
    save_button.grid(row=len(paths) + 1, column=0, columnspan=3, pady=10)

    settings_window.mainloop()

import os
import tkinter as tk
from tkinter import filedialog
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

    # Obter a posição atual da janela principal
    root_x = parent.winfo_x()
    root_y = parent.winfo_y()

    # Posicionar a janela adicional com base na posição da janela principal
    settings_window.geometry(f"+{root_x + 50}+{root_y + 50}")

    # Adicionar um título na parte superior
    title_label = tk.Label(settings_window, text="Configurações", bg='#333333', fg='#8bb7f7', font=('Arial', 16))
    title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

    def save_path(path_key, is_directory=False):
        if is_directory:
            path = filedialog.askdirectory()
        else:
            path = filedialog.askopenfilename(filetypes=(("Link Files", "*.lnk"), 
                                                         ("All Files", "*.*")))
        if path:
            paths[path_key] = remove_quotes(path)
            save_paths()
            path_vars[path_key].set(paths[path_key])

    # Inicializa path_vars com valores do dicionário paths
    path_vars = {key: tk.StringVar(value=paths.get(key, "")) for key in paths}

    for i, (label_text, path_key) in enumerate(paths.items()):
        # Label com texto e fundo da janela
        label = tk.Label(settings_window, text=label_text, bg='#333333', fg='#8bb7f7')
        label.grid(row=i+1, column=0, padx=5, pady=5, sticky="e")

        # Entry para exibir o caminho, com fundo branco e texto preto
        entry = tk.Entry(settings_window, textvariable=path_vars[label_text], width=50, 
                         state='readonly', bg='white', fg='black')
        entry.grid(row=i+1, column=1, padx=5, pady=5)
        ToolTip(entry, f"Defina o caminho para {label_text.lower()}")

        # Botão para procurar o caminho, com fundo cinza escuro e texto branco
        browse_button = tk.Button(settings_window, text="Procurar", 
                                  command=lambda key=label_text: save_path(key),
                                  bg='#444444', fg='#8bb7f7', relief='flat', width=15)
        browse_button.grid(row=i+1, column=2, padx=5, pady=5)

    def copy_file():
        src = filedialog.askopenfilename(title="Selecione o arquivo appserver.ini", 
                                         filetypes=(("INI files", "*.ini"), ("All files", "*.*")))
        if src:
            dst = filedialog.askdirectory(title="Selecione o diretório de destino")
            if dst:
                shutil.copy(src, dst)
                tk.messagebox.showinfo("Sucesso", f"Arquivo copiado para {dst}")

    def save_and_close():
        save_paths()
        settings_window.destroy()

    def close_without_saving():
        settings_window.destroy()

    # Adicionando os botões "Copiar", "Salvar" e "Sair" na mesma linha
    button_frame = tk.Frame(settings_window, bg='#333333')
    button_frame.grid(row=len(paths)+2, column=0, columnspan=3, pady=10)

    copy_button = tk.Button(button_frame, text="Copiar appserver.ini", command=copy_file, 
                            bg='#444444', fg='#8bb7f7', relief='flat', width=15)
    copy_button.pack(side="left", padx=5)

    save_button = tk.Button(button_frame, text="Salvar", command=save_and_close, 
                            bg='#444444', fg='#8bb7f7', relief='flat', width=15)
    save_button.pack(side="left", padx=5)

    exit_button = tk.Button(button_frame, text="Sair", command=close_without_saving, 
                            bg='#444444', fg='#8bb7f7', relief='flat', width=15)
    exit_button.pack(side="left", padx=5)

    # Tornar a janela de configurações modal
    settings_window.transient(parent)
    settings_window.grab_set()
    parent.wait_window(settings_window)
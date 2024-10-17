import os
import requests
import tkinter as tk

def update_rpo(version, log_box, root):
    try:
        # Define a URL e o caminho de destino com base na versão
        if version == "12.1.2210":
            url = "https://arte.engpro.totvs.com.br/protheus/padrao/builds/12.1.2210/latest/repositorio/harpia/tttm120.rpo"
            destino = "C:\\TOTVS\\12.1.2210\\Apo\\TTTM120.RPO"
        elif version == "12.1.2310":
            url = "https://arte.engpro.totvs.com.br/protheus/padrao/builds/12.1.2310/latest/repositorio/harpia/tttm120.rpo"
            destino = "C:\\TOTVS\\12.1.2310\\Apo\\TTTM120.RPO"
        elif version == "12.1.2410":
            url = "https://arte.engpro.totvs.com.br/protheus/padrao/builds/12.1.2410/latest/repositorio/harpia/tttm120.rpo"
            destino = "C:\\TOTVS\\12.1.2410\\Apo\\TTTM120.RPO"
        else:
            log_box.insert(tk.END, "Versão não reconhecida. Atualização do RPO cancelada.\n")
            log_box.yview(tk.END)
            return

        # Função para baixar o arquivo
        def baixar_arquivo(url, destino, log_box):
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()  # Verifica se houve algum erro na requisição

                os.makedirs(os.path.dirname(destino), exist_ok=True)  # Cria o diretório de destino se não existir

                total_size = int(response.headers.get('content-length', 0))  # Tamanho total do arquivo em bytes
                downloaded_size = 0

                log_box.insert(tk.END, "Download em progresso: ")
                log_box.update_idletasks()
                
                with open(destino, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        kb_downloaded = downloaded_size / 1024  # Convertendo bytes para KB
                        log_box.delete('end-1c linestart', 'end-1c lineend')  # Apaga o conteúdo da linha atual
                        log_box.insert(tk.END, f"\rDownload em progresso: {kb_downloaded:.2f} KB")
                        log_box.yview(tk.END)
                        root.update_idletasks()

                log_box.insert(tk.END, f"\nDownload concluído: {destino}\n")
                log_box.yview(tk.END)

            except requests.exceptions.RequestException as e:
                log_box.insert(tk.END, f"\nErro no download: {e}\n")
                log_box.yview(tk.END)

        # Executa o download do RPO
        baixar_arquivo(url, destino, log_box)

    except Exception as e:
        log_box.insert(tk.END, f"Erro na atualização do RPO: {str(e)}\n")
        log_box.yview(tk.END)

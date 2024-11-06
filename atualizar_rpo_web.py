import requests
import os

def update_rpo(version, log_content, update_log):
    """Atualiza o RPO para a versão especificada."""
    try:
        if version == "12.1.2210":
            url = "https://arte.engpro.totvs.com.br/protheus/padrao/builds/12.1.2210/latest/repositorio/harpia/tttm120.rpo"
            destino = "C:\\TOTVS\\12.1.2210\\Apo\\TTTM120.RPO"
        elif version == "12.1.2310":
            url = "https://arte.engpro.totvs.com.br/protheus/padrao/builds/12.1.2310/latest/repositorio/harpia/tttm120.rpo"
            destino = "C:\\TOTVS\\12.1.2310\\Apo\\TTTM120.RPO"
        elif version == "12.1.2410":
            url = "https://arte.engpro.totvs.com.br/protheus/padrao/builds/12.1.2410/latest/repositorio/panthera_onca/tttm120.rpo"
            destino = "C:\\TOTVS\\12.1.2410\\Apo\\TTTM120.RPO"
        else:
            update_log("Versão não reconhecida. Atualização do RPO cancelada.\n")
            return

        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(os.path.dirname(destino), exist_ok=True)

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(destino, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                downloaded_size += len(chunk)
                percent_complete = (downloaded_size / total_size) * 100
                yield f"Baixando: {percent_complete:.2f}% concluído\n"

        yield "Download do RPO concluído.\n"

    except Exception as e:
        yield f"Erro ao atualizar RPO: {str(e)}\n"


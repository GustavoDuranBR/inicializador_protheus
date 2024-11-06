import json
import os

# Dicionário padrão para os caminhos
DEFAULT_PATHS = {
    "Dbaccess": "",
    "Appserver": "",
    "Smartclient": "",
    "Versao_RPO": "12.1.2410"  # Valor padrão da versão RPO
}

def load_paths():
    """Carrega os caminhos de paths.json ou retorna o dicionário padrão se não existir."""
    if os.path.exists("paths.json"):
        try:
            with open("paths.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Erro ao ler paths.json. Usando configurações padrão.")
            return DEFAULT_PATHS
    return DEFAULT_PATHS

def save_paths(paths):
    """Salva o dicionário paths em paths.json."""
    try:
        with open("paths.json", "w") as file:
            json.dump(paths, file, indent=4)
    except IOError as e:
        print(f"Erro ao salvar paths.json: {e}")

def initialize_paths(version=None):
    """Inicializa os caminhos com base na versão RPO fornecida ou salva no arquivo."""
    paths = load_paths()
    
    # Definir a versão RPO
    if not version:
        version = paths["Versao_RPO"] or DEFAULT_PATHS["Versao_RPO"]
    paths["Versao_RPO"] = version  # Atualiza a versão no dicionário
    
    # Atualizar os caminhos dos executáveis com a versão selecionada
    paths["Dbaccess"] = "C:\\TOTVS\\TotvsDBAccess\\dbaccess64.exe - Atalho.lnk"
    paths["Appserver"] = f"C:\\TOTVS\\Protheus_{version}\\bin\\Appserver\\appserver.exe - Atalho.lnk"
    paths["Smartclient"] = f"C:\\TOTVS\\Protheus_{version}\\bin\\SmartClient\\smartclient.exe - Atalho.lnk"
    
    # Salva as configurações atualizadas
    save_paths(paths)
    return paths

# Carregar e inicializar os caminhos
paths = initialize_paths()

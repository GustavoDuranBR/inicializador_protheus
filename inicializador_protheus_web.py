import streamlit as st
import subprocess
from atualizar_rpo_web import update_rpo
from config_web import paths, save_paths, load_paths

# Carregar configurações iniciais
paths = load_paths()

# Definindo o ícone da aba
st.set_page_config(
    page_title="Inicializador Protheus",  # Título da aba
    page_icon="TOTS3.SA.ico",  # Caminho para o ícone
    layout="wide"
)

# Inicializando o log_content se não estiver definido
if 'log_content' not in st.session_state:
    st.session_state.log_content = []
if 'progress_content' not in st.session_state:
    st.session_state.progress_content = ""

# Define um espaço vazio para o log e os botões
button_display = st.empty()  # Espaço reservado para os botões
log_display = st.empty()     # Espaço reservado para o log

def update_log(message, is_progress=False):
    if is_progress:
        st.session_state.progress_content = message
    else:
        st.session_state.log_content.append(message)
    display_logs()

def display_logs():
    log_content = '\n'.join(st.session_state.log_content)
    full_log_content = log_content + "\n" + st.session_state.progress_content
    if log_content:
        log_display.markdown(
            f"""
            <div style="background-color: black; color: #00FF00; font-family: monospace; padding: 10px; 
                        border-radius: 5px; height: 400px; width: 800px; overflow-y: auto; margin-top: 20px;">
                {full_log_content.replace("</div>", "")}
            """,
            unsafe_allow_html=True
        )
    else:
        log_display.markdown(
            """
            <div style="background-color: black; color: #00FF00; font-family: monospace; padding: 10px; 
                        border-radius: 5px; height: 400px; width: 800px; overflow-y: auto; margin-top: 20px;">
                O log está vazio.
            """,
            unsafe_allow_html=True
        )

def run_command(command):
    update_log(f"Iniciando: {command}...\n")
    
    try:
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            for stdout_line in iter(process.stdout.readline, ""):
                if stdout_line:
                    update_log(stdout_line.strip())
            process.stdout.close()
            return_code = process.wait()
            if return_code:
                update_log(f"<span style='color:red;'>Erro: Código de saída {return_code}</span>\n")
            else:
                update_log("Finalizado com sucesso.\n")
    except Exception as e:
        update_log(f"<span style='color:red;'>Erro ao executar comando: {e}</span>\n")

def start_dbaccess_and_appserver():
    dbaccess_command = f'start "" "{paths["Dbaccess"]}"'
    appserver_command = f'start "" "{paths["Appserver"]}"'
    run_command(dbaccess_command)
    run_command(appserver_command)

def start_update_rpo():
    version = paths.get("Versao_RPO", "")
    if not version:
        update_log("<span style='color:red;'>Erro: Versão RPO não está definida. Verifique nas Configurações.</span>\n")
        return
    update_log("Iniciando atualização do RPO...\n")
    
    progress_updates = update_rpo(version, st.session_state.log_content, lambda msg: update_log(msg, is_progress=True)) or []
    
    for progress in progress_updates:
        update_log(progress, is_progress=True)
    
    update_log("RPO baixado com sucesso.\n", is_progress=True)

def close_terminals():
    update_log("Fechando terminais...\n")
    dbaccess_close_command = "taskkill /F /IM dbaccess64.exe"
    appserver_close_command = "taskkill /F /IM appserver.exe"

    # Execute os comandos de fechamento de forma síncrona
    def safe_run_command(command):
        run_command(command)
        update_log(f"<span style='color:green;'>Terminal para {command.split('/IM ')[-1]} fechado com sucesso.</span>\n")
    
    try:
        safe_run_command(dbaccess_close_command)
        safe_run_command(appserver_close_command)
        update_log("<span style='color:red;'>Todos os terminais foram fechados.</span>\n")
    except Exception as e:
        update_log(f"<span style='color:red;'>Erro ao fechar terminais: {e}</span>\n")

# Sidebar para configurações
st.sidebar.header("Configurações")
version_options = ["12.1.2210", "12.1.2310", "12.1.2410"]
selected_version = st.sidebar.selectbox("Selecionar Versão RPO", version_options)

# Adicionar opções de upload
uploaded_appserver_file = st.sidebar.file_uploader("Carregar appserver.ini", type="ini")
uploaded_rpo_file = st.sidebar.file_uploader("Carregar TTTM120.RPO", type="rpo")

# Salvar arquivos em pastas específicas
if uploaded_appserver_file is not None:
    appserver_path = f"C:\\TOTVS\\Protheus_{selected_version}\\bin\\Appserver\\{uploaded_appserver_file.name}"  # ajuste o caminho conforme necessário
    with open(appserver_path, "wb") as f:
        f.write(uploaded_appserver_file.getbuffer())
    st.sidebar.success(f"Arquivo {uploaded_appserver_file.name} salvo com sucesso!")

if uploaded_rpo_file is not None:
    rpo_path = f"C:\\TOTVS\\{selected_version}\\Apo\\{uploaded_rpo_file.name}"  # ajuste o caminho conforme necessário
    with open(rpo_path, "wb") as f:
        f.write(uploaded_rpo_file.getbuffer())
    st.sidebar.success(f"Arquivo {uploaded_rpo_file.name} salvo com sucesso!")

if selected_version:
    paths["Versao_RPO"] = selected_version
    paths["Appserver"] = f"C:\\TOTVS\\Protheus_{selected_version}\\bin\\Appserver\\appserver.exe - Atalho.lnk"
    paths["Smartclient"] = f"C:\\TOTVS\\Protheus_{selected_version}\\bin\\SmartClient\\smartclient.exe - Atalho.lnk"

st.sidebar.text_input("Caminho para DbAccess", value=paths["Dbaccess"], disabled=True)
st.sidebar.text_input("Caminho para AppServer", value=paths["Appserver"], disabled=True)
st.sidebar.text_input("Caminho para SmartClient", value=paths["Smartclient"], disabled=True)

if st.sidebar.button("Salvar Configurações"):
    save_paths(paths)
    st.sidebar.success("Configurações salvas com sucesso!")

# CSS customizado para padronizar o estilo dos botões
st.markdown("""
    <style>
    .button-container button {
        width: 100%;
        height: 50px;
        font-size: 16px;
    }
    .title-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Informações sobre versão e desenvolvedor
st.sidebar.markdown(f"**Dev**: Gustavo Duran  \n**Versão**: 1.0")

# Botões principais
with button_display.container():
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("TOTS3.SA.ico", width=70)
    with col2:
        st.markdown("<div class='title-container'><h1>Inicializador Protheus</h1></div>", unsafe_allow_html=True)

    col3, col4, col5, col6 = st.columns(4, gap="small")
    with col3:
        if st.button("DbAccess/AppServer", key="btn1", use_container_width=True):
            start_dbaccess_and_appserver()
    with col4:
        if st.button("Protheus WEB", key="btn2", use_container_width=True):
            web_url = "http://localhost:8089"
            try:
                subprocess.Popen(f'start {web_url}', shell=True)
                update_log(f"Navegador aberto em {web_url}.\n")
            except Exception as e:
                update_log(f"<span style='color:red;'>Erro ao abrir o navegador: {e}</span>")
    with col5:
        if st.button("Atualizar RPO", key="btn3", use_container_width=True):
            start_update_rpo()
    with col6:
        if st.button("Fechar Terminais", key="btn4", use_container_width=True):
            close_terminals()

# Exibir o log abaixo dos botões
display_logs()

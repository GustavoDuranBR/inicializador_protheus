# Inicializador Protheus

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-3776AB?style=for-the-badge&logo=requests&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-3C7EBB?style=for-the-badge&logo=tkinter&logoColor=white)

Este projeto é uma aplicação web para facilitar a execução de tarefas relacionadas ao Protheus. Ele permite o gerenciamento de serviços, como `DbAccess` e `AppServer`, através de uma interface gráfica web e apresenta logs em tempo real, com visual customizável, para o acompanhamento das operações.

## Funcionalidades

- **Iniciar e Reiniciar Serviços:** Botão para iniciar ou reiniciar simultaneamente o `DbAccess` e o `AppServer`.
- **Monitoramento em Tempo Real:** Logs atualizados em tempo real, exibindo o progresso de download e execução de tarefas.
- **Configuração e Persistência de Caminhos:** Permite configurar e salvar os caminhos dos executáveis do Protheus, facilitando o acesso e a execução.
- **Atualização do RPO:** Download e atualização da versão do RPO diretamente da interface, com acompanhamento do progresso.
- **Exibição Personalizada de Logs:** Interface inspirada em PowerShell para logs, com visual de cores similar ao Git Bash.
- **Encerramento Automático de Serviços:** Todos os serviços iniciados são encerrados ao sair do programa ou ao clicar em "Fechar Terminais".

## Tecnologias Utilizadas

- **Python:** Lógica principal da aplicação.
- **Flask:** Estrutura de back-end da aplicação web.
- **Streamlit:** Interface gráfica para exibir a aplicação na web.
- **Requests:** Manipulação e gerenciamento de requisições HTTP para download do RPO.
- **JSON:** Armazenamento e carregamento de configurações persistentes.
- **Tkinter:** Interface inicial, agora substituída por Streamlit para uma experiência web.
- **PowerShell (visual):** Para simular a aparência de logs na interface Streamlit.

## Requisitos

- Python 3.6 ou superior
- Flask e Streamlit
- Requests
- (Opcional) Tkinter para testes locais

## Instalação

### 1. Clonar o Repositório

```sh
git clone https://github.com/seuusuario/projeto_inicializador_protheus.git
cd projeto_inicializador_protheus
```

### 2. Criar e Ativar um Ambiente Virtual

```sh
python -m venv venv

# No Windows
venv\Scripts\activate

# No macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependências

```sh
pip install -r requirements.txt
```

## Uso

### Executar a Aplicação Web

Para iniciar o aplicativo de inicialização do Protheus, execute:

```sh
streamlit run inicializador_protheus.py
```

Isso abrirá uma interface web onde você poderá gerenciar serviços, monitorar logs e atualizar o RPO.

### Configuração dos Caminhos

Para configurar os caminhos dos executáveis do `DbAccess`, `AppServer`, e `SmartClient`:

1. Acesse a interface web na aba de configurações.
2. Selecione os arquivos e caminhos desejados.
3. Salve as configurações para uso persistente.

### Atualização do RPO

Na aba de atualização, selecione a versão desejada do RPO e inicie o download. Acompanhe o progresso na área de logs.

---

### Documentação de Configurações

Para mais informações sobre as configurações de diretórios e como configurar corretamente o sistema, consulte a [documentação de configurações](docs/CONFIGURACOES_DIRETORIOS.md).

---

## Estrutura do Projeto

```plaintext
projeto_inicializador_protheus/
│
├── venv/                         # Diretório do ambiente virtual
├── inicializador_protheus.py     # Lógica principal da aplicação
├── config.py                     # Gerenciamento de configurações
├── paths.json                    # Armazena caminhos configurados
├── requirements.txt              # Dependências do projeto
└── .gitignore                    # Arquivos e diretórios ignorados pelo Git
```

## Contribuição

Sinta-se à vontade para contribuir com o projeto. Você pode abrir uma *issue* ou enviar um *pull request*.

### Como Contribuir

1. Faça um *fork* do projeto.
2. Crie uma *branch* para sua *feature* ou correção (`git checkout -b minha-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Push para a *branch* (`git push origin minha-feature`).
5. Abra um *Pull Request*.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Para dúvidas ou suporte, entre em contato através do email gustavoduran22@gmail.com
# Menu de Tarefas do Protheus
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Este projeto é um aplicativo de interface gráfica desenvolvido em Python para facilitar a execução de
várias tarefas relacionadas ao Protheus.
Ele permite a execução de comandos, abertura de navegadores e configuração de caminhos de arquivos.

## Funcionalidades

- Iniciar Dbaccess
- Iniciar Appserver
- Iniciar Protheus WEB
- Iniciar Smartclient
- Atualização do RPO
- Configurar caminhos para cada tarefa
- Copiar arquivo `appserver.ini` para um diretório específico

## Requisitos

- Python 3.6 ou superior
- tkinter (geralmente incluído na instalação padrão do Python)

## Instalação

### 1. Clonar o Repositório

```sh
https://github.com/GustavoDuranBR/inicializador_protheus
cd repositoryname
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
pip install tk
```

## Uso

### Executar o Programa

```sh
python inicializador_protheus.py
```

### Configuração

Para configurar os caminhos dos executáveis e outras configurações:

1. Clique no botão "Configurações".
2. Na nova janela, defina os caminhos desejados.
3. Salve as configurações.

### Copiar `appserver.ini`

Na aba de configurações, você pode selecionar o arquivo `appserver.ini` e o diretório de destino para copiá-lo:

1. Clique no botão Copiar appserver.ini
2. Selecione o `appserver.ini` que deseja utilizar
3. Selecione o diretório padrão para executar o appserver
4. O programa copiar o `appserver.ini` devidamente

## Estrutura do Projeto

```plaintext
project/
│
├── venv/                      # Diretório da virtual environment
├── inicializador_protheus.py  # Lógica principal da aplicação
├── config.py                  # Lógica da janela de configurações
├── tooltip.py                 # Classe para dicas de ferramentas
├── requirements.txt           # Arquivo de dependências
└── .gitignore                 # Arquivo para ignorar arquivos/diretórios específicos no Git
```

## Contribuição

Se você encontrar bugs ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

### Como Contribuir

1. Faça um fork do projeto.
2. Crie uma branch para sua feature ou correção de bug (`git checkout -b minha-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Push para a branch (`git push origin minha-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Se tiver dúvidas ou precisar de ajuda, entre em contato através do email gustavoduran22@gmail.com


# TFiles

# Gerenciador de arquivos via terminal

Gerenciador de arquivos simples para Linux que roda em linha de comando, proporcionando uma maneira simples e eficaz de fazer coisas como copiar, mover, recortar, renomear e etc.

Requisitos minimos para rodar:
    
    Python3.7+
    Qualquer sistema que rode bash

![shocase1](https://user-images.githubusercontent.com/67431981/106668939-aea66f00-6589-11eb-8361-66c09275910b.png)

    

    Simbolos

    [•] Arquivo de texto
    [>] Arquivo de aplicação
    [𝄞] Arquivo de áudio
    [▶] Arquivo de vídeo
    [☀] Arquivo de imagem
    [𝕥] Arquivo de fonte
    [?] Arquivo genérico ou binário
    [0] Arquivo binário
    [+] Diretório

    Comandos

    / Voltar ao diretório passado
    /* Atualizar configurações e o diretório atual
    /a Criar um arquivo
    /bash Tela de comandos bash para ações mais complexas
    /cln Tela de comando rápido
    /cor Trocar a cor do gerenciador de arquivos
    /d Criar um diretório
    /deco Troca a decoração de titulo
    /del Apagar um diretório
    /e Sair
    /fdel Apagar um arquivo
    /h Vai para a pasta home do user atual
    /help Exibe essa tela
    /i Informações de um arquivo ou diretório
    /info Informações do TFiles
    /k Copiar e colar um arquivo ou diretório
    /l Lê um arquivo e exibe seu conteúdo
    /m Mover um arquivo/diretório
    /md Ir para /media/{usuário atual}
    /r Ir para a pasta root
    /rename Renomear um arquivo/diretório
    /reset Restaura as configurações de design para o padrão
    /search Pesquisa por arquivos/diretórios que contenham uma string especifica
    /usrbin Ir para /usr/bin
    /texto Editor de texto (Básico, recomendado apenas para edições simples)
        OBS: .help para ajuda em comandos.
    Apenas "ENTER" volta dois diretórios

## Como instalar/desinstalar
    Para instalar:
        chmod +x install.sh
        sudo ./install.sh
        Isso criará um comando chamado "tfiles" e copiará os arquivos 'cdt' e 'tfiles.py' para '/opt/tfiles/'.
    Para desinstalar
        chmod +x unistall.sh
        sudo ./unistall.sh

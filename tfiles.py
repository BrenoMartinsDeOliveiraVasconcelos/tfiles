try:
    # Caminho e comandos
    import os
    import getpass
    import shutil
    import random
    import linecache
    import readline
    import clipboard
    import mimetypes
    import time

    hhaa = os.popen('stty size', 'r').read().split()
    vsf = int(hhaa[1])
    guest = False
    os.system("clear")
    title = linecache.getline('/opt/tfiles/cdt', 1).replace('\n', '')



    def get_size(start_path = '.'):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            dirnames = dirnames
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    if not os.path.islink(fp):
                        if 'kcore' != f:
                            total_size += os.path.getsize(fp)
                except FileNotFoundError:
                    pass

        return total_size


    def last(letra, twices=2):
        if twices == 2:
            for we in range(0, 2):
                we = we
                del letra[-1]
        elif twices == 1:
            del letra[-1]
        elif twices == 3:
            for we in range(0, 3):
                del letra[-1]

        return letra


    def enter():
        valordeinput = input("\033[37mENTER para continuar.")
        return valordeinput


    def clear():
        os.system("clear")


    run = 0

    completepath = []
    path = os.getcwd().split('/')
    for peti in path:
        completepath.append(f'/{peti}')
    path = completepath[:]

    prepath = ''
    contents = os.listdir(''.join(path))
    errorstatus = 0
    nextpath = ''
    n = ''
    a = ''
    c = ''
    pular = False
    exilio = False
    errortipo = 'Nulo'
    gado = []
    gado2 = []
    narnia = ''
    darosinal = False
    corno = 0
    manso = -1
    corno2 = -2
    rango = 0
    dobreak = False
    errorstatusdev = 0

    decos = str(''.join((open("/opt/tfiles/deco", 'r').readlines())).replace("\n", '')).split(' ')
    comandos = ['/', '/a', '/d', '/e', '/h', '/k', '/l', '/m', '/r', '/fdel', '/del', '/rename', '/*', '/info', '/md',
                '/usrbin', '/texto', '/cor', '/deco', '/reset', '/bash', '/cln', '/search', '/i']
    while True:
        if run == 0:
            pass
        else:
            if getpass.getuser() == 'root':
                print('')
                print("\033[31mCuidado! TFiles está em modo root.", end='')
            print(f"\033[{title}m", end='')
            print("")
            print(f'{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4), end='')
            if len(path) > 1:
                nextpath = input(f"""Onder ir agora?
Caminho: {''.join(path[1:])}/""")
            else:
                nextpath = input(f"""Onde ir agora?
Caminho: {''.join(path)}""")
            if nextpath == 'dev':
                errorstatusdev = 1
            nextpath = nextpath.split('/')
            if nextpath[0] == '':
                nextpath[0] = '/'
            print(f'{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4))
            if errorstatusdev == 1:
                errorstatusdev = 0
            print('\u001b[37m')
            for loop in range(0, len(contents)):
                if ''.join(nextpath) == contents[loop] or ''.join(nextpath) in comandos:
                    errorstatus = 0
                    break
                else:
                    errorstatus = 1
            prepath = path[:]
            for sla in nextpath:
                path.append(f'/{sla}')
            commandpath = ''.join(nextpath)
            if path[0] == '/':
                if commandpath == '/':
                    try:
                        path = last(path, twices=3)
                    except IndexError:
                        pass
                elif commandpath == '/d':
                    path = last(path)
                    n = str(input("Nome do diretório: "))
                    try:
                        os.mkdir(f"{''.join(path)}/{n}")
                    except PermissionError:
                        print(f"\033[31mPermissão negada.")
                        enter()
                    except FileExistsError:
                        print(f"\033[31mDiretório já existe.")
                        enter()
                    except OSError:
                        print('\033[31mOcorreu um erro.')
                        enter()
                elif commandpath == '/a':
                    path = last(path)
                    n = str(input("Nome do arquivo: "))
                    if n not in contents:
                        try:
                            open(f'{"".join(path)}/{n}', 'w+')
                        except IsADirectoryError:
                            print(f"\033[31mIsso é um diretório, pare.")
                            enter()
                        except PermissionError:
                            print(f"\033[31mPermissão negada.")
                            enter()
                        except OSError:
                            print('\033[31mOcorreu um erro.')
                            enter()
                    else:
                        print(f"\033[31mArquivo já existe.")
                elif commandpath == '/e':
                    print('\033[0m', end='')
                    exit()
                elif commandpath == '/del':
                    path = last(path)
                    n = str(input("Nome do diretório: "))
                    if n == "/":
                        print("HEY! PERMISSÃO NEGADA!")
                        exit()
                    else:
                        os.system(f'rm -r "{"""""".join(path)}/{n}" >/dev/null 2>&1')
                elif commandpath == '/fdel':
                    path = last(path)
                    n = str(input("Nome do arquivo: "))
                    try:
                        os.remove(f"{''.join(path)}/{n}")
                    except PermissionError:
                        print(f"\033[31mPermissão negada.")
                        enter()
                    except FileNotFoundError:
                        print(f"\033[31mArquivo inexistente.")
                        enter()
                    except OSError:
                        print('\033[31mOcorreu um erro.')
                        enter()
                elif commandpath == '/r':
                    path = last(path)
                    path = ['/']
                elif commandpath == '/k':
                    path = last(path)
                    src = str(input("Nome do arquivo/diretório a copiar: "))
                    dst = str(input("Local a colar: "))
                    try:
                        shutil.copyfile(f"{''.join(path)}/{src}", f"{dst}/{src}")
                    except IsADirectoryError:
                        try:
                            shutil.copytree(f"{''.join(path)}/{src}", f'{dst}/{src}')
                        except FileExistsError:
                            try:
                                shutil.copyfile(f"{''.join(path)}/{src}", f"{dst}/{src}-{random.randint(0, 999)}")
                            except IsADirectoryError:
                                print(f"\033[31mOperação cancelada.")
                                enter()
                        except IsADirectoryError:
                            print(f"\033[31mOperação cancelada.")
                            enter()
                    except FileNotFoundError:
                        print(f"\033[31mArquivo/diretório não encontrado.")
                        enter()
                    except PermissionError:
                        print(f"\033[31mPermissão negada.")
                        enter()
                    except OSError:
                        print('\033[31mOcorreu um erro.')
                        enter()
                elif commandpath == '/m':
                    path = last(path)
                    src = str(input("Nome do arquivo/diretório a mover: "))
                    dst = str(input("Local de destino: "))
                    if dst and src != '':
                        try:
                            shutil.move(f'{"".join(path)}/{src}', f'{dst}/{src}')
                        except FileNotFoundError:
                            print(f"\033[31mArquivo/diretório não encontrado.")
                            enter()
                        except PermissionError:
                            print(f"\033[31mPermissão negada.")
                            enter()
                        except OSError:
                            print('\033[31mOcorreu um erro.')
                            enter()
                    else:
                        pass
                elif commandpath == '/rename':
                    path = last(path)
                    src = str(input("Nome do arquivo/diretório a renomear: "))
                    dst = str(input("Novo nome: "))
                    try:
                        os.rename(f'{"".join(path)}/{src}', f'{"".join(path)}/{dst}')
                    except FileNotFoundError:
                        print(f"\033[31mArquivo/diretório não encontrado.")
                        enter()
                    except PermissionError:
                        print(f"\033[31mPermissão negada.")
                        enter()
                    except OSError:
                        print('\033[31mOcorreu um erro.')
                        enter()
                elif commandpath == '/h':
                    if getpass.getuser() != 'root':
                        path = ['/', '/home', f'/{getpass.getuser()}']
                    else:
                        path = ['/', '/root']

                    if guest:
                        path = ['/', '/home']
                elif commandpath == '/help':
                    print("""

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
    /i Informações sobre algum arquivo ou diretório
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

                    """)
                    path = last(path)
                    enter()
                elif commandpath == '/l':
                    path = last(path)
                    arquivo = str(input("Arquivo: "))
                    try:
                        y = open(f'{"".join(path)}/{arquivo}', 'r')
                        print(''.join(y.readlines()))
                        enter()
                    except IsADirectoryError:
                        print('\033[31;1mNão é um arquivo.')
                        enter()
                    except PermissionError:
                        print('\033[31;1mPermissão negada.')
                        enter()
                    except UnicodeDecodeError:
                        print('\033[31;1mApenas arquivos de texto são legiveis!')
                        enter()
                    except FileNotFoundError:
                        print('\033[31;1mArquivo não encontrado.')
                        enter()
                    except OSError:
                        print('\033[31;1mOcorreu um erro.')
                        enter()
                elif commandpath == '/*':
                    path = last(path)
                    decos = str(''.join((open("/opt/tfiles/deco", 'r').readlines())).replace("\n", '')).split(' ')
                    title = "".join(open("/opt/tfiles/cdt", 'r').readlines()).replace("\n", "")
                elif commandpath == '/info':
                    path = last(path)
                    print("TFiles v1.4.0b")
                    print("Desenvolvedor: Breno Martins de Oliveira Vasconcelos")
                    print(
                        "GitHub: https://github.com/BrenoMartinsDeOliveiraVasconcelos/Terminal-Files-Manager/tree/main/"
                    )
                    enter()
                elif commandpath == '/md':
                    path = ['/', '/media', f'/{getpass.getuser()}']
                elif commandpath == '/nada':
                    path = last(path, twices=1)
                elif commandpath == '/usrbin':
                    path = ['/', '/usr', '/bin']
                elif commandpath == '/texto':
                    path = last(path)
                    arquivo = ''
                    cancelar = False
                    while True:
                        arquivo = input('Arquivo de texto: ')
                        try:
                            w = open(f'{"".join(path)}/{arquivo}', 'r')
                            break
                        except FileNotFoundError:
                            try:
                                w = open(f'{"".join(path)}/{arquivo}', 'w+')
                                w.close()
                                w = open(f'{"".join(path)}/{arquivo}', 'r')
                                break
                            except PermissionError:
                                print('\033[31mPermissão negada ao tentar criar arquivo inexistente.')
                                cancelar = True
                                break
                        except PermissionError:
                            print('\033[31mPermissão negada.')
                            cancelar = True
                            break
                        except IsADirectoryError:
                            print('\033[31mÉ um diretório.')
                            cancelar = True
                            break
                        except UnicodeDecodeError:
                            print('\033[31mNão é um arquivo de texto.')
                            cancelar = True
                            break
                    clear()
                    quebrar = False
                    nsv = False
                    while not cancelar:
                        pathdotreco = f"{''.join(path[1:])}/{arquivo}/"
                        print(f'\033[{title}m{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4))
                        print(f'\033[{title}m{f"Editor de Texto":^{vsf}}')
                        print(f'\033[{title}m{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4))
                        print('\n')
                        try:
                            texto = w.readlines()
                        except UnicodeDecodeError:
                            print('\033[31mO-oh! Parece que isso não é um arquivo de texto...')
                            enter()
                            w.close()
                            break
                        w.close()
                        line = 0
                        firstrun = -1
                        for cont in texto:
                            line = line + 1
                            print(f'\033[{title}m[{line}]\033[37m {cont}', end='')
                        while True:
                            if firstrun == -1:
                                line = line + 1
                                ca = input(f"\033[{title}m[{line}]\033[37m ")
                            else:
                                clear()
                                print(
                                    f'\033[{title}m{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}'* int(int(vsf)/4)
                                )
                                print(f'\033[{title}m{f"Editor de Texto":^80}')
                                print(
                                    f'\033[{title}m{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4))
                                print('\n')
                                line = 0
                                for cont in texto:
                                    line = line + 1
                                    print(f'\033[{title}m[{line}]\033[37m {cont}', end='')
                                ca = input(f"\033[{title}m[{line + 1}]\033[37m ")
                            texto.append(f'{ca}\n')
                            firstrun = firstrun + 1
                            if texto[-1] == '.stop\n':
                                del texto[-1]
                                quebrar = True
                                break
                            elif texto[-1] == '.dl\n':
                                del texto[-1]
                                try:
                                    linedel = int(input('Número da linha: ')) - 1
                                    del texto[linedel]
                                except (TypeError, ValueError, IndexError):
                                    pass
                            elif texto[-1] == '.help\n':
                                del texto[-1]
                                print("""
                            
    .al Adiciona um número especifico de linhas com um texto especificado
    .cancel Sai sem salvar
    .clear Limpa o arquivo de texto, apagando todo seu conteudo mas mantendo o arquivo
    .dl Deleta uma linha
    .dlnum Deleta númericamente especifico as últimas linhas 
    .el Edita uma linha
    .help Tela de ajuda do editor de textos
    .stop Salva e fecha o arquivo
    .whereami Mostra o caminho do arquivo atual

    OBS: Para adicionar comandos como texto normal, adicione espaço antes ou depois do tal comando

                                """)
                                enter()
                            elif texto[-1] == '.el\n':
                                del texto[-1]
                                try:
                                    editar = int(input("Linha: ")) - 1
                                except (ValueError, TypeError):
                                    editar = -1
                                try:
                                    texto[editar] = f'{input(f"[{editar + 1}] ")}\n'
                                except IndexError:
                                    print('\033[31mLinha inexistente!')
                                    enter()
                            elif texto[-1] == '.al\n':
                                del texto[-1]
                                textolinhas = f"{input('Texto: ')}\n"
                                try:
                                    nlinhas = int(input("Número de linhas: "))
                                except (TypeError, ValueError):
                                    nlinhas = 1

                                for kabanga in range(0, nlinhas):
                                    texto.append(textolinhas)
                            elif texto[-1] == '.dlnum\n':
                                del texto[-1]
                                while True:
                                    try:
                                        numl = int(input("Número de linhas a deletar: "))
                                        break
                                    except (ValueError, TypeError):
                                        print('\033[31mIsso não é um número!\033[37m')
                                for deletador in range(0, numl + 1):
                                    try:
                                        del texto[-1]
                                    except IndexError:
                                        break
                            elif texto[-1] == '.clear\n':
                                texto = []
                            elif texto[-1] == '.whereami\n':
                                del texto[-1]
                                print(pathdotreco)
                                enter()
                            elif texto[-1] == '.cancel\n':
                                del texto[-1]
                                quebrar = True
                                nsv = True
                                break
                        if quebrar:
                            if not nsv:
                                try:
                                    w = open(f'{"".join(path)}/{arquivo}', 'w')
                                    w.write(''.join(texto))
                                    w.close()
                                except PermissionError:
                                    print('\033[31mAcesso de escrita negado.')
                                    enter()
                                    w.close()
                            else:
                                w.close()
                            break
                elif commandpath == '/cor':
                    path = last(path)
                    confirmar = False
                    print("\033[37mSelecione a cor desejada.")
                    while not confirmar:
                        for coresid in range(0, 8):
                            print(f'ID: {coresid}, resultado: \033[3{coresid}m123\033[37m')
                        while True:
                            try:
                                cordousuario = int(input("\033[37mID da cor desejada: "))
                                break
                            except (ValueError, TypeError):
                                print("\033[31mIsso não é um ID!")
                                pass
                        while str(cordousuario) not in '01234567':
                            try:
                                cordousuario = int(input("\033[31mCor inválida. ID da cor desejada: "))
                            except (ValueError, TypeError):
                                cordousuario = int(input("\033[31mApenas números podem ser aceitos. ID da cor desejada: "))
                        print("Ok, o resultado final será mais ou menos este:")
                        print(f'\033[3{cordousuario}m{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4))
                        print(f'\033[3{cordousuario}m{"Gerenciador de Arquivos":^{vsf}}')
                        print(f'\033[3{cordousuario}m{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4))
                        print('')
                        print(
                            '\033[37mUbuntu Linux Live USB \033[32m[+]                \033[37mSansumgDisk 1TB \033[32m[+]')
                        print('')
                        print(f'\033[3{cordousuario}m{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4))
                        print(f"\033[3{cordousuario}mCaminho: /media/Lucas/")
                        print(f'\033[3{cordousuario}m{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4))
                        confirmarao = input(
                            f"\033[37mTem certeza que deseja aplicar a cor de id \033[3{cordousuario}m{cordousuario}\033[37m? [S/N] ")
                        while confirmarao not in 'SsNn':
                            confirmarao = input(
                                f"\033[37mTem certeza que deseja aplicar a cor de id \033[3{cordousuario}m{cordousuario}\033[37m? [S/N] ")
                        if confirmarao in 'Ss':
                            title = int(f'3{cordousuario}')
                            try:
                                cor = open("/opt/tfiles/cdt", 'w')
                                cor.write(f'3{cordousuario}')
                                cor.close()
                            except PermissionError:
                                print(
                                    "\033[31mVocê precisa rodar esse comando como root (em sudo) para alterar isso permanentemente. (O arquivo de configuração está em (/opt/tfiles/)")
                                enter()
                            confirmar = True
                        else:
                            pass
                elif commandpath == '/deco':
                    times = 0
                    notexecute = False
                    path = last(path)
                    confirmar = False
                    while not confirmar:
                        stringd = input("String decorativa (separar cada caractére por espaço): ")
                        while ' ' not in stringd:
                            times = times + 1
                            if times < 3:
                                stringd = input("String decorativa (PONHA PELO MENOS 1 ESPAÇO): ")
                            else:
                                notexecute = True
                                break
                        if not notexecute:
                            print('Ficará algo do tipo: ')
                            sample = stringd.split(" ")
                            print(
                                f"\033[{title}m{random.choice(sample)}{random.choice(sample)}{random.choice(sample)}" * int(int(vsf)/4))
                            print(f"\033[{title}m{'Gerenciador de Arquivos':^60}")
                            print(
                                f"\033[{title}m{random.choice(sample)}{random.choice(sample)}{random.choice(sample)}" * int(int(vsf)/4))
                            print('')
                            print(f'\033[37mLucas \033[32m[+]                              \033[37mEduardo \033[32m[+]')
                            print('')
                            print(
                                f"\033[{title}m{random.choice(sample)}{random.choice(sample)}{random.choice(sample)}" * int(int(vsf)/4))
                            print("Caminho: /home/")
                            print(f"{random.choice(sample)}{random.choice(sample)}{random.choice(sample)}" * int(int(vsf)/4))
                            confirm = ' '
                            while confirm not in 'SsNn':
                                confirm = input("\033[37mConfirmar? [S/N] ")
                            if confirm in 'Ss':
                                break
                            else:
                                pass
                        else:
                            break
                    if not notexecute:
                        try:
                            acb = open("/opt/tfiles/deco", 'w')
                            acb.write(stringd)
                            acb.close()
                        except PermissionError:
                            print('\033[31mVocê precisa de previlégios de administrador para editar arquivos em /opt.')
                            enter()
                    else:
                        pass
                elif commandpath == '/reset':
                    path = last(path)
                    print('\033[31mIsso vai restaurar TODAS as configruações para o padrão de fábrica.')
                    continuarisso = input("Você deseja prosseguir com a operação? Isso não pode ser desfeito! [S/N] ")
                    if len(continuarisso) > 0:
                        if continuarisso in 'Ss':
                            print('')
                            abrir = ['/opt/tfiles/deco', '/opt/tfiles/cdt']
                            for reset in abrir:
                                if reset == abrir[0]:
                                    rest = open(reset, 'w')
                                    rest.write("⚘ = * •")
                                    rest.close()
                                elif reset == abrir[1]:
                                    rest = open(reset, 'w')
                                    rest.write("33")
                                    rest.close()
                            print("\033[32m/* para surtir efeito.")
                            enter()
                    else:
                        pass
                elif commandpath == '/cln':
                    path = last(path)
                    os.system(input("Commando: "))
                    enter()
                elif commandpath == '/bash':
                    path = last(path)
                    os.system("bash --version")
                    print("Para sair, basta digitar 'exit'.")
                    print("\033[0m")
                    os.system("bash")
                    enter()
                elif commandpath == '/search':
                    path = last(path)
                    query = input("Procurar arquivs/diretórios que contenham: ")
                    tem = False
                    parece = []
                    pontos = 0
                    for procurar in contents:
                        pontos = 0
                        if procurar == query:
                            tem = True
                            parece.append(query)
                        else:
                            if query.upper() in procurar.upper():
                                parece.append(procurar)
                    if tem:
                        print('\033[32mExiste um arquivo/diretório com o exato nome digitado.')
                    else:
                        pass
                    if len(parece) > 1:
                        crtz = input(f"\033[{title}mDeseja exibir todos os \033[35m{len(parece)} \033[{title}marquivos/diretórios encontrados? ")
                    else:
                        if len(parece) == 1:
                            crtz = input(f"\033[{title}mDeseja exibir o arquivo/diretório encontrado? ")
                        else:
                            crtz = ''
                    numb = 0
                    if crtz in 'Ss':
                        clear()
                        for xablau in parece:
                            tipo = mimetypes.guess_type(f"{''.join(path)}/{xablau}")
                            try:
                                if 'text' in tipo[0]:
                                    symb = '\033[35m[•]'
                                elif 'application' in tipo[0]:
                                    symb = "\033[36m[>]"
                                elif 'audio' in tipo[0]:
                                    symb = '\033[33m[𝄞]'
                                elif 'video' in tipo[0]:
                                    symb = '\033[30m[▶]'
                                elif 'image' in tipo[0]:
                                    symb = "\033[33m[☀]"
                                elif 'font' in tipo[0]:
                                    symb = '\033[35m[𝕥]'
                            except (TypeError, ValueError):
                                if os.path.isfile(f"{''.join(path)}/{xablau}") and not os.path.isdir(f"{''.join(path)}/{xablau}"):
                                    symb = '\033[34m[?]'
                                elif os.path.isdir(f"{''.join(path)}/{xablau}") and not os.path.isfile(f"{''.join(path)}/{xablau}"):
                                    symb = '\033[32m[+]'
                                else:
                                    symb = '\033[34m[0]'
                            numb = numb+1
                            print(f'\033[{title}m[{numb}] \033[37m{xablau} {symb}\033[37m')
                        aiai = input('Deseja copiar algum nome de arquivo/diretório? ')
                        if aiai in 'Ss' and aiai != '':
                            while True:
                                try:
                                    clipboard.copy(parece[int(input("ID: "))-1])
                                    break
                                except IndexError:
                                    print("\033[31mID inválido.")
                                except (TypeError, ValueError):
                                    print("\033[31mID é um número, não outra coisa.")
                                except KeyError:
                                    print("\033[31mAtualmente, essa função não funciona em modo root :/")
                                    break
                    enter()
                elif commandpath == '/i':
                    path = last(path)
                    forms = ['byte(s)', 'kilobyte(s)', 'megabyte(s)', 'gigabyte(s)', 'terrabyte(s)', 'petabyte(s)', '']
                    while True:
                        arqv = input("Arquivo: ")
                        try:
                            if not os.path.isdir(f"{''.join(path)}/{arqv}"):
                                sz = os.stat(f"{''.join(path)}/{arqv}").st_size
                            else:
                                sz = get_size(f"{''.join(path)}/{arqv}")
                            original = sz
                            break
                        except FileNotFoundError:
                            print("\033[31mArquivo não encontrado :/")
                    backsz = 0
                    form = 0
                    frmt = ''
                    while True:
                        if sz > 1024:
                            try:
                                sz = sz / 1024
                                form = form + 1
                                frmt = forms[form]
                            except IndexError:
                                frmt = forms[form]
                                break
                        else:
                            frmt = forms[form]
                            break
                    print(f"""              
Caminho: {''.join(path[1:])}/{arqv}
Tipo: {mimetypes.guess_type(f'{"".join(path)}/{arqv}')[0]}
Tamanho: {sz:.0f} {frmt} ({original} byte(s))
Criado: {time.ctime(os.path.getctime(f"{''.join(path)}/{arqv}"))}
Modificado: {time.ctime(os.path.getmtime(f"{''.join(path)}/{arqv}"))}
                    """)
                    enter()

            else:
                path = ['/']
            try:
                contents = os.listdir(''.join(path))
                errorstatus = 0
            except NotADirectoryError:
                path = prepath[:]
                errorstatus = 1
                errortipo = 'Tipo'
            except FileNotFoundError:
                path = prepath[:]
                errorstatus = 1
                errortipo = 'Nome'
            except PermissionError:
                path = prepath[:]
                errorstatus = 1
                errortipo = 'Root'
        run = run + 1
        texto = []
        if errorstatus == 0:
            hhaa = os.popen('stty size', 'r').read().split()
            vsf = int(hhaa[1])
            # Exibir conteudo do diretório
            clear()
            print(f'\033[1;{title}m', end='')
            print(f'{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4))
            print(f"\033[1;{title}m{'Gerenciador de Arquivos':^{vsf}}")
            print(f'{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}{random.choice(decos)}' * int(int(vsf)/4))
            contents = sorted(contents)
            for loop in range(0, len(contents)):
                gado2.append(contents[loop])
                tipo = mimetypes.guess_type(f"{''.join(path)}/{contents[loop]}")
                try:
                    if 'text' in tipo[0]:
                        gado2.append('\033[35m[•]')
                    elif 'application' in tipo[0]:
                        gado2.append("\033[36m[>]")
                    elif 'audio' in tipo[0]:
                        gado2.append('\033[33m[𝄞]')
                    elif 'video' in tipo[0]:
                        gado2.append('\033[30m[▶]')
                    elif 'image' in tipo[0]:
                        gado2.append("\033[33m[☀]")
                    elif 'font' in tipo[0]:
                        gado2.append('\033[35m[𝕥]')
                except (TypeError, ValueError):
                    if os.path.isfile(f"{''.join(path)}/{contents[loop]}") and not os.path.isdir(f"{''.join(path)}/{contents[loop]}"):
                        gado2.append('\033[34m[?]')
                    elif os.path.isdir(f"{''.join(path)}/{contents[loop]}") and not os.path.isfile(f"{''.join(path)}/{contents[loop]}"):
                        gado2.append('\033[32m[+]')
                    else:
                        gado2.append('\033[34m[0]')
                gado.append(' '.join(gado2))
                gado2 = []
            print('\033[37;1m')
            for corno in range(0, len(gado)):
                manso = manso + 2
                corno2 = corno2 + 2
                if len(gado) > 1:
                    try:
                        a = gado[corno2]
                    except IndexError:
                        rango = 'end'
                    try:
                        c = gado[manso]
                    except IndexError:
                        rango = 'end'
                elif len(gado) == 1:
                    a = ''.join(gado)
                    c = ''
                else:
                    a = 'Diretório vazio :/'
                    c = ''
                if rango != 'end' or c == gado[-1]:
                    print(f"\033[37;1m{a:<30}\033[37;1m{c:>{vsf-20}}")
                    if c == gado[-1]:
                        break
                else:
                    print(f'\033[37;1m{gado[-1]}')
                    break
            gado = []
            manso = -1
            corno2 = -2
            rango = 0
            # Erros
        else:
            if errortipo == 'Nome':
                wuhan = path[:]
                print(f'\033[31m\nOcorreu um erro! Verifique a ortografia e tente novamente.')
                enter()
            elif errortipo == 'Tipo':
                print(f'\033[31m\n"{"""""".join(path[1:])}/{commandpath}" não é um diretório!')
                enter()
            elif errortipo == 'Root':
                print(f'\033[31m\nVocê não tem permissão para acessar "{"""""".join(path[1:])}/{commandpath}".')
                enter()
except KeyboardInterrupt:
    print("\n\033[0m")

#!/usr/bin/env python3
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
    import keyboard
    import sys

    terminal_size = os.popen('stty size', 'r').read().split()
    terminal_width = int(terminal_size[1])
    is_guest = False
    os.system("clear")
    sys.argv.append('')


    def get_directory_size(start_path = '.'):
        count = 0
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            dirnames = dirnames
            count = count + 1
            try:
                if keyboard.is_pressed("c"):
                    break
            except ImportError:
                if count == 1:
                    print("\033[31mDevido a uma limitação do Linux, 'c' para cancelar só é possivel via root.\033[37m")
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    if not os.path.islink(file_path):
                        if 'kcore' != filename:
                            total_size += os.path.getsize(file_path)
                except FileNotFoundError:
                    pass

        return total_size


    def remove_last_items(item_list, times=2):
        for _ in range(0, times):
            del item_list[-1]

        return item_list


    def wait_for_enter():
        input_value = input("\033[37mENTER para continuar.")
        return input_value


    def clear_screen():
        os.system("clear")


    run_count = 0

    complete_path = []
    if sys.argv[1] == '':
        current_path = os.getcwd().split('/')
    else:
        try:
            current_path = sys.argv[1].split('/')
            os.listdir(f'/{sys.argv[1]}')
        except FileNotFoundError:
            print("\033[1;31mIsso não é um caminho válido! Peço que escreva o caminho completo caso esteja correto.")
            exit()
        except PermissionError:
            print("\033[1;31mEsse diretório só é acessivel em modo root.")
            exit()
        except NotADirectoryError:
            print("\033[1;31mEsse diretório só é acessivel em modo root.")
            exit()
    for path_item in current_path:
        complete_path.append(f'/{path_item}')
    current_path = complete_path[:]

    previous_path = ''
    directory_contents = os.listdir(''.join(current_path))
    error_status = 0
    next_command = ''
    n = ''
    a = ''
    c = ''
    skip_flag = False
    exile_flag = False
    error_type = 'Nulo'
    display_items = []
    temp_display = []
    display_metadata = []
    signal_flag = False
    display_counter = 0
    left_index = -1
    right_index = -2
    range_counter = 0
    break_flag = False
    dev_error_status = 0

    commands = ['/', '/a', '/d', '/e', '/h', '/k', '/l', '/m', '/r', '/fdel', '/del', '/rename', '/*', '/info', '/md',
                '/usrbin', '/texto', '/bash', '/cln', '/search', '/i', '/shexec', '/full']
    while True:
        if run_count == 0:
            pass
        else:
            print('')
            columns = int(terminal_size[0])
            columns_total = int(columns - (3 + 2 + ((len(directory_contents) / 2) - 0.1)))
            columns_wasted = 0
            pretty_display = []
            columns_total = columns_total - 1
            if columns_total > 1:
                os.system('setterm -background white -foreground white')
                columns_text = f''
                print(f"\033[1;30m{columns_text}", end='')
                print(' '* int(terminal_width - len(columns_text)))
                os.system('setterm -background black -foreground black')
                for _ in range(1, columns_total):
                    print(f'{"Apenas isso por enquanto":^{terminal_width}}')
            else:
                pass
            if run_count > 1:
                os.system("setterm -background white -foreground white")
                print(" "*terminal_width)
                os.system('setterm -background black -foreground black')
                print(f'\033[1;37mOnde ir agora?')
                os.system('setterm -background black -foreground black')
                next_command = input(f"""\033[1;37mCaminho: {''.join(current_path[1:])}/""")
            else:
                next_command = '/*'
                os.system('setterm -background black foreground white')
                for _ in range(0, 10000):
                    print("")
                clear_screen()
            if next_command == 'dev':
                dev_error_status = 1
                
            if next_command.strip("\n") == '':
                next_command = '/*'
                
            next_command = next_command.split('/')
            if next_command[0] == '':
                next_command[0] = '/'
            if dev_error_status == 1:
                dev_error_status = 0
            print('\u001b[37m')
            for index in range(0, len(directory_contents)):
                if ''.join(next_command) == directory_contents[index] or ''.join(next_command) in commands:
                    error_status = 0
                    break
                else:
                    error_status = 1
            previous_path = current_path[:]
            for item in next_command:
                current_path.append(f'/{item}')
            command_path = ''.join(next_command)
            if current_path[0] == '/':
                if command_path == '/':
                    try:
                        current_path = remove_last_items(current_path, times=2)
                    except IndexError:
                        pass
                elif command_path == '/d':
                    current_path = remove_last_items(current_path)
                    n = str(input("Nome do diretório: "))
                    try:
                        os.mkdir(f"{''.join(current_path)}/{n}")
                    except PermissionError:
                        print(f"\033[31mPermissão negada.")
                        wait_for_enter()
                    except FileExistsError:
                        print(f"\033[31mDiretório já existe.")
                        wait_for_enter()
                    except OSError:
                        print('\033[31mOcorreu um erro.')
                        wait_for_enter()
                elif command_path == '/a':
                    current_path = remove_last_items(current_path)
                    n = str(input("Nome do arquivo: "))
                    if n not in directory_contents:
                        try:
                            open(f'{"".join(current_path)}/{n}', 'w+')
                        except IsADirectoryError:
                            print(f"\033[31mIsso é um diretório, pare.")
                            wait_for_enter()
                        except PermissionError:
                            print(f"\033[31mPermissão negada.")
                            wait_for_enter()
                        except OSError:
                            print('\033[31mOcorreu um erro.')
                            wait_for_enter()
                    else:
                        print(f"\033[31mArquivo já existe.")
                elif command_path == '/e':
                    print('\033[0m', end='')
                    os.system("setterm -default")
                    clear_screen()
                    exit()
                elif command_path == '/del':
                    current_path = remove_last_items(current_path)
                    n = str(input("Nome do diretório: "))
                    if n == "/":
                        print("HEY! PERMISSÃO NEGADA!")
                        exit()
                    else:
                        os.system(f'rm -r "{"""""".join(current_path)}/{n}" >/dev/null 2>&1')
                elif command_path == '/fdel':
                    current_path = remove_last_items(current_path)
                    n = str(input("Nome do arquivo: "))
                    try:
                        os.remove(f"{''.join(current_path)}/{n}")
                    except PermissionError:
                        print(f"\033[31mPermissão negada.")
                        wait_for_enter()
                    except FileNotFoundError:
                        print(f"\033[31mArquivo inexistente.")
                        wait_for_enter()
                    except OSError:
                        print('\033[31mOcorreu um erro.')
                        wait_for_enter()
                elif command_path == '/r':
                    current_path = remove_last_items(current_path)
                    current_path = ['/']
                elif command_path == '/k':
                    current_path = remove_last_items(current_path)
                    src = str(input("Nome do arquivo/diretório a copiar: "))
                    dst = str(input("Local a colar: "))
                    try:
                        shutil.copyfile(f"{''.join(current_path)}/{src}", f"{dst}/{src}")
                    except IsADirectoryError:
                        try:
                            shutil.copytree(f"{''.join(current_path)}/{src}", f'{dst}/{src}')
                        except FileExistsError:
                            try:
                                shutil.copyfile(f"{''.join(current_path)}/{src}", f"{dst}/{src}-{random.randint(0, 999)}")
                            except IsADirectoryError:
                                print(f"\033[31mOperação cancelada.")
                                wait_for_enter()
                        except IsADirectoryError:
                            print(f"\033[31mOperação cancelada.")
                            wait_for_enter()
                    except FileNotFoundError:
                        print(f"\033[31mArquivo/diretório não encontrado.")
                        wait_for_enter()
                    except PermissionError:
                        print(f"\033[31mPermissão negada.")
                        wait_for_enter()
                    except OSError:
                        print('\033[31mOcorreu um erro.')
                        wait_for_enter()
                elif command_path == '/m':
                    current_path = remove_last_items(current_path)
                    src = str(input("Nome do arquivo/diretório a mover: "))
                    dst = str(input("Local de destino: "))
                    if dst and src != '':
                        try:
                            shutil.move(f'{"".join(current_path)}/{src}', f'{dst}/{src}')
                        except FileNotFoundError:
                            print(f"\033[31mArquivo/diretório não encontrado.")
                            wait_for_enter()
                        except PermissionError:
                            print(f"\033[31mPermissão negada.")
                            wait_for_enter()
                        except OSError:
                            print('\033[31mOcorreu um erro.')
                            wait_for_enter()
                    else:
                        pass
                elif command_path == '/rename':
                    current_path = remove_last_items(current_path)
                    src = str(input("Nome do arquivo/diretório a renomear: "))
                    dst = str(input("Novo nome: "))
                    try:
                        os.rename(f'{"".join(current_path)}/{src}', f'{"".join(current_path)}/{dst}')
                    except FileNotFoundError:
                        print(f"\033[31mArquivo/diretório não encontrado.")
                        wait_for_enter()
                    except PermissionError:
                        print(f"\033[31mPermissão negada.")
                        wait_for_enter()
                    except OSError:
                        print('\033[31mOcorreu um erro.')
                        wait_for_enter()
                elif command_path == '/h':
                    if getpass.getuser() != 'root':
                        current_path = ['/', '/home', f'/{getpass.getuser()}']
                    else:
                        current_path = ['/', '/root']

                    if is_guest:
                        current_path = ['/', '/home']
                elif command_path == '/help':
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
/d Criar um diretório
/del Apagar um diretório
/e Sair
/fdel Apagar um arquivo
/full Exibe o nome de um arquivo sem corte
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
/search Pesquisa por arquivos/diretórios que contenham uma string especifica
/shexec Executa um arquivo em shell
/usrbin Ir para /usr/bin
/texto Editor de texto (Básico, recomendado apenas para edições simples)
    OBS: .help para ajuda em comandos.
Apenas "ENTER" volta dois diretórios

                    """)
                    current_path = remove_last_items(current_path)
                    wait_for_enter()
                elif command_path == '/l':
                    current_path = remove_last_items(current_path)
                    file_name = str(input("Arquivo: "))
                    try:
                        file_handle = open(f'{"".join(current_path)}/{file_name}', 'r')
                        line_count = 0
                        for line in file_handle.readlines():
                            line_count = line_count + 1
                            print(f"\033[33m[{line_count}] \033[37m{line}", end='')
                        wait_for_enter()
                    except IsADirectoryError:
                        print('\033[31;1mNão é um arquivo.')
                        wait_for_enter()
                    except PermissionError:
                        print('\033[31;1mPermissão negada.')
                        wait_for_enter()
                    except UnicodeDecodeError:
                        print('\033[31;1mApenas arquivos de texto são legiveis!')
                        wait_for_enter()
                    except FileNotFoundError:
                        print('\033[31;1mArquivo não encontrado.')
                        wait_for_enter()
                    except OSError:
                        print('\033[31;1mOcorreu um erro.')
                        wait_for_enter()
                elif command_path == '/*':
                    current_path = remove_last_items(current_path)
                elif command_path == '/info':
                    current_path = remove_last_items(current_path)
                    print("TFiles v1.0.0")
                    print("Desenvolvedor: Breno Martins de Oliveira Vasconcelos")
                    print(
                        "GitHub: https://github.com/BrenoMartinsDeOliveiraVasconcelos/tfiles"
                    )
                    wait_for_enter()
                elif command_path == '/md':
                    current_path = ['/', '/media', f'/{getpass.getuser()}']
                elif command_path == '/nada':
                    current_path = remove_last_items(current_path, times=1)
                elif command_path == '/usrbin':
                    current_path = ['/', '/usr', '/bin']
                elif command_path == '/texto':
                    current_path = remove_last_items(current_path)
                    file_name = ''
                    cancel_flag = False
                    while True:
                        file_name = input('Arquivo de texto: ')
                        try:
                            file_handle = open(f'{"".join(current_path)}/{file_name}', 'r')
                            break
                        except FileNotFoundError:
                            try:
                                file_handle = open(f'{"".join(current_path)}/{file_name}', 'w+')
                                file_handle.close()
                                file_handle = open(f'{"".join(current_path)}/{file_name}', 'r')
                                break
                            except PermissionError:
                                print('\033[31mPermissão negada ao tentar criar arquivo inexistente.')
                                cancel_flag = True
                                break
                        except PermissionError:
                            print('\033[31mPermissão negada.')
                            cancel_flag = True
                            break
                        except IsADirectoryError:
                            print('\033[31mÉ um diretório.')
                            cancel_flag = True
                            break
                        except UnicodeDecodeError:
                            print('\033[31mNão é um arquivo de texto.')
                            cancel_flag = True
                            break
                    clear_screen()
                    exit_flag = False
                    no_save_flag = False
                    while not cancel_flag:
                        full_path = f"{''.join(current_path[1:])}/{file_name}/"
                        os.system('setterm -background white -foreground white')
                        print(f"\033[1;30m{'Terminal Explorer':^{terminal_width}}")
                        os.system('setterm -background black foreground black')
                        print("")
                        try:
                            text_content = file_handle.readlines()
                        except UnicodeDecodeError:
                            print('\033[31mO-oh! Parece que isso não é um arquivo de texto...')
                            wait_for_enter()
                            file_handle.close()
                            break
                        file_handle.close()
                        line_num = 0
                        first_run = -1
                        for line_content in text_content:
                            line_num = line_num + 1
                            print(f'\033[33m[{line_num}]\033[37m {line_content}', end='')
                        while True:
                            if first_run == -1:
                                line_num = line_num + 1
                                command_input = input(f"\033[33m[{line_num}]\033[37m ")
                            else:
                                clear_screen()
                                os.system('setterm -background white -foreground white')
                                print(f"\033[1;30m{'Terminal Explorer':^{terminal_width}}")
                                os.system('setterm -background black -foreground black')
                                print('')
                                line_num = 0
                                for line_content in text_content:
                                    line_num = line_num + 1
                                    print(f'\033[33m[{line_num}]\033[37m {line_content}', end='')
                                command_input = input(f"\033[33m[{line_num + 1}]\033[37m ")
                            text_content.append(f'{command_input}\n')
                            first_run = first_run + 1
                            if text_content[-1] == '.exit\n':
                                del text_content[-1]
                                exit_flag = True
                                break
                            elif text_content[-1] == '.dl\n':
                                del text_content[-1]
                                try:
                                    line_to_delete = int(input('Número da linha: ')) - 1
                                    del text_content[line_to_delete]
                                except (TypeError, ValueError, IndexError):
                                    pass
                            elif text_content[-1] == '.help\n':
                                del text_content[-1]
                                print("""
                            
.al Adiciona um número especifico de linhas com um texto especificado
.cancel Sai sem salvar
.clear Limpa o arquivo de texto, apagando todo seu conteudo mas mantendo o arquivo
.dl Deleta uma linha
.dlnum Deleta númericamente especifico as últimas linhas 
.el Edita uma linha
.exit Salva e fecha o arquivo
.help Tela de ajuda do editor de textos
.save Salva o arquivo sem fechar
.search Procura algum texto especifico
.whereami Mostra o caminho do arquivo atual

    OBS: Para adicionar comandos como texto normal, adicione espaço antes ou depois do tal comando

                                """)
                                wait_for_enter()
                            elif text_content[-1] == '.el\n':
                                del text_content[-1]
                                try:
                                    edit_line = int(input("Linha: ")) - 1
                                except (ValueError, TypeError):
                                    edit_line = -1
                                try:
                                    text_content[edit_line] = f'{input(f"[{edit_line + 1}] ")}\n'
                                except IndexError:
                                    print('\033[31mLinha inexistente!')
                                    wait_for_enter()
                            elif text_content[-1] == '.al\n':
                                del text_content[-1]
                                line_text = f"{input('Texto: ')}\n"
                                try:
                                    num_lines = int(input("Número de linhas: "))
                                except (TypeError, ValueError):
                                    num_lines = 1

                                for _ in range(0, num_lines):
                                    text_content.append(line_text)
                            elif text_content[-1] == '.dlnum\n':
                                del text_content[-1]
                                while True:
                                    try:
                                        num_lines = int(input("Número de linhas a deletar: "))
                                        break
                                    except (ValueError, TypeError):
                                        print('\033[31mIsso não é um número!\033[37m')
                                for _ in range(0, num_lines + 1):
                                    try:
                                        del text_content[-1]
                                    except IndexError:
                                        break
                            elif text_content[-1] == '.clear\n':
                                text_content = []
                            elif text_content[-1] == '.whereami\n':
                                del text_content[-1]
                                print(full_path)
                                wait_for_enter()
                            elif text_content[-1] == '.cancel\n':
                                del text_content[-1]
                                exit_flag = True
                                no_save_flag = True
                                break
                            elif text_content[-1] == '.save\n':
                                del text_content[-1]
                                try:
                                    file_handle = open(f'{"".join(current_path)}/{file_name}', 'w')
                                    file_handle.write(''.join(text_content))
                                    file_handle.close()
                                except PermissionError:
                                    print('\033[31mAcesso de escrita negado.')
                                    wait_for_enter()
                                    file_handle.close()
                            elif text_content[-1] == '.search\n':
                                del text_content[-1]
                                search_query = input("Pesquisar: ")
                                line_num = 0
                                match_count = 0
                                matches = []
                                for line in text_content:
                                    line_num = line_num + 1
                                    if search_query in line:
                                        match_count = match_count + 1
                                        print(f'\033[32mEncontrado \033[35m"{search_query}"\033[32m na linha {line_num}.')
                                    else:
                                        pass
                                print(f"\033[37mAo todo, foram encontrados resultados em \033[32m{match_count} \033[37mlinhas.")
                                wait_for_enter()
                        if exit_flag:
                            if not no_save_flag:
                                try:
                                    file_handle = open(f'{"".join(current_path)}/{file_name}', 'w')
                                    file_handle.write(''.join(text_content))
                                    file_handle.close()
                                except PermissionError:
                                    print('\033[31mAcesso de escrita negado.')
                                    wait_for_enter()
                                    file_handle.close()
                            else:
                                file_handle.close()
                            break
                elif command_path == '/cln':
                    current_path = remove_last_items(current_path)
                    os.system(input("Commando: "))
                    wait_for_enter()
                elif command_path == '/bash':
                    current_path = remove_last_items(current_path)
                    os.system("bash")
                    wait_for_enter()
                elif command_path == '/search':
                    current_path = remove_last_items(current_path)
                    query = input("Procurar arquivs/diretórios que contenham: ")
                    found_flag = False
                    matches = []
                    points = 0
                    for item in directory_contents:
                        points = 0
                        if item == query:
                            found_flag = True
                            matches.append(query)
                        else:
                            if query.upper() in item.upper():
                                matches.append(item)
                    if found_flag:
                        print('\033[32mExiste um arquivo/diretório com o exato nome digitado.')
                    else:
                        pass
                    if len(matches) > 1:
                        confirm = input(f"\033[32mDeseja exibir todos os \033[35m{len(matches)} \033[32marquivos/diretórios encontrados? ")
                    else:
                        if len(matches) == 1:
                            confirm = input(f"\033[32mDeseja exibir o arquivo/diretório encontrado? ")
                        else:
                            confirm = ''
                    num_item = 0
                    if confirm in 'Ss':
                        clear_screen()
                        for item_name in matches:
                            file_type = mimetypes.guess_type(f"{''.join(current_path)}/{item_name}")
                            try:
                                if 'text' in file_type[0]:
                                    symbol = '\033[35m[•]'
                                elif 'application' in file_type[0]:
                                    symbol = "\033[36m[>]"
                                elif 'audio' in file_type[0]:
                                    symbol = '\033[33m[𝄞]'
                                elif 'video' in file_type[0]:
                                    symbol = '\033[30m[▶]'
                                elif 'image' in file_type[0]:
                                    symbol = "\033[33m[☀]"
                                elif 'font' in file_type[0]:
                                    symbol = '\033[35m[𝕥]'
                            except (TypeError, ValueError):
                                if os.path.isfile(f"{''.join(current_path)}/{item_name}") and not os.path.isdir(f"{''.join(current_path)}/{item_name}"):
                                    symbol = '\033[34m[?]'
                                elif os.path.isdir(f"{''.join(current_path)}/{item_name}") and not os.path.isfile(f"{''.join(current_path)}/{item_name}"):
                                    symbol = '\033[32m[+]'
                                else:
                                    symbol = '\033[34m[0]'
                            num_item = num_item+1
                            print(f'\033[33m[{num_item}] \033[37m{item_name} {symbol}\033[37m')
                        copy_confirm = input('Deseja copiar algum nome de arquivo/diretório? ')
                        if copy_confirm in 'Ss' and copy_confirm != '':
                            while True:
                                try:
                                    clipboard.copy(matches[int(input("ID: "))-1])
                                    break
                                except IndexError:
                                    print("\033[31mID inválido.")
                                except (TypeError, ValueError):
                                    print("\033[31mID é um número, não outra coisa.")
                                except KeyError:
                                    print("\033[31mAtualmente, essa função não funciona em modo root :/")
                                    break
                    wait_for_enter()
                elif command_path == '/i':
                    current_path = remove_last_items(current_path)
                    units = ['byte(s)', 'kilobyte(s)', 'megabyte(s)', 'gigabyte(s)', 'terrabyte(s)', 'petabyte(s)', '']
                    while True:
                        file_name = input("Arquivo: ")
                        try:
                            if not os.path.isdir(f"{''.join(current_path)}/{file_name}"):
                                size = os.stat(f"{''.join(current_path)}/{file_name}").st_size
                            else:
                                size = get_directory_size(f"{''.join(current_path)}/{file_name}")
                            original_size = size
                            break
                        except FileNotFoundError:
                            print("\033[31mArquivo não encontrado :/")
                    backup_size = 0
                    unit_index = 0
                    unit_format = ''
                    while True:
                        if size > 1024:
                            try:
                                size = size / 1024
                                unit_index = unit_index + 1
                                unit_format = units[unit_index]
                            except IndexError:
                                unit_format = units[unit_index]
                                break
                        else:
                            unit_format = units[unit_index]
                            break
                    print(f"""              
Caminho: {''.join(current_path[1:])}/{file_name}
Tipo: {mimetypes.guess_type(f'{"".join(current_path)}/{file_name}')[0]}
Tamanho: {size:.0f} {unit_format} ({original_size} byte(s))
Criado: {time.ctime(os.path.getctime(f"{''.join(current_path)}/{file_name}"))}
Modificado: {time.ctime(os.path.getmtime(f"{''.join(current_path)}/{file_name}"))}
                    """)
                    wait_for_enter()
                elif command_path == '/shexec':
                    current_path = remove_last_items(current_path)
                    sudo_confirm = input("Sudo? [S/N]")
                    if sudo_confirm in "Ss":
                        run_sudo = 'sudo'
                    else:
                        run_sudo = ''
                    file_name = input("Arquivo: ")
                    os.system(f"{run_sudo} sh {''.join(current_path)}/{file_name}")
                    wait_for_enter()
                elif command_path == '/full':
                    current_path = remove_last_items(current_path)
                    directory_contents = sorted(os.listdir(f"{''.join(current_path)}"))
                    file_id = -1
                    for item in directory_contents:
                        file_id = file_id + 1
                        print(f"[{file_id+1}] {item}")
                    wait_for_enter()
            else:
                current_path = ['/']
            try:
                directory_contents = os.listdir(''.join(current_path))
                error_status = 0
            except NotADirectoryError:
                current_path = previous_path[:]
                error_status = 1
                error_type = 'Tipo'
            except FileNotFoundError:
                current_path = previous_path[:]
                error_status = 1
                error_type = 'Nome'
            except PermissionError:
                current_path = previous_path[:]
                error_status = 1
                error_type = 'Root'
        run_count = run_count + 1
        text_content = []
        if error_status == 1:
            if error_type == 'Nome':
                temp_path = current_path[:]
                print(f'\033[31m\nOcorreu um erro! Verifique a ortografia e tente novamente.')
                wait_for_enter()
            elif error_type == 'Tipo':
                print(f'\033[31m\n"{"""""".join(current_path[1:])}/{command_path}" não é um diretório!')
                wait_for_enter()
            elif error_type == 'Root':
                print(f'\033[31m\nVocê não tem permissão para acessar "{"""""".join(current_path[1:])}/{command_path}".')
                wait_for_enter()
        terminal_size = os.popen('stty size', 'r').read().split()
        terminal_width = int(terminal_size[1])
        continue_flag = True
        # Exibir conteudo do diretório
        if run_count == 1:
            continue_flag = False
        clear_screen()
        if continue_flag:
            os.system('setterm -background white -foreground white')
            if getpass.getuser() != 'root':
                print(f"\033[1;30m{'Terminal Explorer':^{terminal_width}}")
            else:
                print(f"\033[1;30m{'Terminal Explorer (ROOT)':^{terminal_width}}")
            os.system('setterm -background black foreground black')
            directory_contents = sorted(directory_contents)
            new_loop = []
            for item in directory_contents:
                char_count = 0
                if len(item) > 15:
                    for char in item:
                        char_count = char_count + 1
                        if char_count <= 15:
                            new_loop.append(char)
                        else:
                            new_loop.append('...')
                            break
                    new_loop = ''.join(new_loop)
                    temp_display.append(new_loop)
                else:
                    temp_display.append(item)
                new_loop = []
                file_type = mimetypes.guess_type(f"{''.join(current_path)}/{item}")
                try:
                    if 'text' in file_type[0]:
                        temp_display.append('\033[35m[•]')
                    elif 'application' in file_type[0]:
                        temp_display.append("\033[36m[>]")
                    elif 'audio' in file_type[0]:
                        temp_display.append('\033[33m[𝄞]')
                    elif 'video' in file_type[0]:
                        temp_display.append('\033[30m[▶]')
                    elif 'image' in file_type[0]:
                        temp_display.append("\033[33m[☀]")
                    elif 'font' in file_type[0]:
                        temp_display.append('\033[35m[𝕥]')
                except (TypeError, ValueError):
                    if os.path.isfile(f"{''.join(current_path)}/{item}") and not os.path.isdir(f"{''.join(current_path)}/{item}"):
                        temp_display.append('\033[34m[?]')
                    elif os.path.isdir(f"{''.join(current_path)}/{item}") and not os.path.isfile(f"{''.join(current_path)}/{item}"):
                        temp_display.append('\033[32m[+]')
                    else:
                        temp_display.append('\033[34m[0]')
                display_items.append(' '.join(temp_display))
                temp_display = []
            print('\033[37;1m')
            for index in range(0, len(display_items)):
                left_index = left_index + 2
                right_index = right_index + 2
                if len(display_items) > 1:
                    try:
                        a = display_items[right_index]
                    except IndexError:
                        range_counter = 'end'
                    try:
                        c = display_items[left_index]
                    except IndexError:
                        range_counter = 'end'
                elif len(display_items) == 1:
                    a = ''.join(display_items)
                    c = ''
                else:
                    a = 'Diretório vazio :/'
                    c = ''
                if range_counter != 'end' or c == display_items[-1]:
                    print(f"\033[37;1m{a:<30}\033[37;1m{c:>{terminal_width-20}}")
                    if c == display_items[-1]:
                        break
                else:
                    print(f'\033[37;1m{display_items[-1]}')
                    break
            display_metadata = display_items[:]
            display_items = []
            left_index = -1
            right_index = -2
            range_counter = 0
except KeyboardInterrupt:
    print("\n\033[0m")
    os.system("setterm -default")
    os.system("clear")
    exit()

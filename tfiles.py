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
    import helpers as h

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
                    h.print_error("\033[31mDevido a uma limitação do Linux, 'c' para cancelar só é possivel via root.\033[37m")
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





    def clear_screen():
        os.system("clear")

    def main():
        run_count = 0

        complete_path = []
        if sys.argv[1] == '':
            current_path = os.getcwd().split('/')
        else:
            try:
                current_path = sys.argv[1].split('/')
                os.listdir(f'/{sys.argv[1]}')
            except FileNotFoundError:
                h.print_error("Isso não é um caminho válido! Peço que escreva o caminho completo caso esteja correto.", quit=True)
            except PermissionError:
                h.print_error("Esse diretório só é acessivel em modo root.", quit=True)
            except NotADirectoryError:
                h.print_error("Esse diretório só é acessivel em modo root.", quit=True)
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
                h.output('')
                columns = int(terminal_size[0])
                columns_total = int(columns - (3 + 2 + ((len(directory_contents) / 2) - 0.1)))
                columns_wasted = 0
                pretty_display = []
                columns_total = columns_total - 1
                if columns_total > 1:
                    h.print_separator(terminal_width)
                    for _ in range(1, columns_total):
                        h.output(f'{"Apenas isso por enquanto":^{terminal_width}}', color_code="\033[1;30m")
                else:
                    pass
                if run_count > 1:
                    h.switch_emptiness(black=False)
                    h.output(" "*terminal_width)
                    h.switch_emptiness(black=True)
                    h.output(f'\033[1;37mOnde ir agora?')
                    h.switch_emptiness(black=True)
                    next_command = h.ask_input(f"Caminho: {''.join(current_path[1:])}/")
                else:
                    next_command = '/*'
                    h.switch_font_blackness(black=False)
                    for _ in range(0, 10000):
                        h.output("")
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
                    auto_skip = False
                    if command_path == '/':
                        try:
                            current_path = remove_last_items(current_path, times=3)
                            auto_skip = True
                        except IndexError:
                            pass
                    elif command_path == '/d':
                        current_path = remove_last_items(current_path)
                        n = h.ask_input("Nome do diretório: ")
                        try:
                            os.mkdir(f"{''.join(current_path)}/{n}")
                        except PermissionError:
                            h.print_error(f"Permissão negada.")
                        except FileExistsError:
                            h.print_error(f"Diretório já existe.")
                        except OSError:
                            h.print_error('Ocorreu um erro.')
                    elif command_path == '/a':
                        current_path = remove_last_items(current_path)
                        n = h.ask_input("Nome do arquivo: ")
                        if n not in directory_contents:
                            try:
                                open(f'{"".join(current_path)}/{n}', 'w+')
                            except IsADirectoryError:
                                h.print_error(f"Isso é um diretório, pare.")
                            except PermissionError:
                                h.print_error(f"Permissão negada.")
                            except OSError:
                                h.print_error('Ocorreu um erro.')
                        else:
                            h.print_error("Arquivo já existe.")
                    elif command_path == '/e':
                        h.output('', end='', color_code="\033[0m")
                        h.restore_setterm()
                        clear_screen()
                        exit()
                    elif command_path == '/del':
                        current_path = remove_last_items(current_path)
                        n = h.ask_input("Nome do diretório: ")
                        if n == "/":
                            h.print_error("Permissão negada!")
                        else:
                            os.system(f'rm -r "{"""""".join(current_path)}/{n}" >/dev/null 2>&1')
                    elif command_path == '/fdel':
                        current_path = remove_last_items(current_path)
                        n = h.ask_input("Nome do arquivo: ")
                        try:
                            os.remove(f"{''.join(current_path)}/{n}")
                        except PermissionError:
                            h.print_error(f"Permissão negada.")
                        except FileNotFoundError:
                            h.print_error(f"Arquivo inexistente.")
                        except OSError:
                            h.print_error('Ocorreu um erro.')
                    elif command_path == '/r':
                        current_path = remove_last_items(current_path)
                        current_path = ['/']
                    elif command_path == '/k':
                        current_path = remove_last_items(current_path)
                        src = h.ask_input("Nome do arquivo/diretório a copiar: ")
                        dst = h.ask_input("Local a colar: ")
                        try:
                            shutil.copyfile(f"{''.join(current_path)}/{src}", f"{dst}/{src}")
                        except IsADirectoryError:
                            try:
                                shutil.copytree(f"{''.join(current_path)}/{src}", f'{dst}/{src}')
                            except FileExistsError:
                                try:
                                    shutil.copyfile(f"{''.join(current_path)}/{src}", f"{dst}/{src}-{random.randint(0, 999)}")
                                except IsADirectoryError:
                                    h.print_error(f"Operação cancelada.")
                            except IsADirectoryError:
                                h.print_error("Operação cancelada.")
                        except FileNotFoundError:
                            h.print_error(f"Arquivo/diretório não encontrado.")
                        except PermissionError:
                            h.print_error(f"Permissão negada.")
                        except OSError:
                            h.print_error('Ocorreu um erro.')
                    elif command_path == '/m':
                        current_path = remove_last_items(current_path)
                        src = h.ask_input("Nome do arquivo/diretório a mover: ")
                        dst = h.ask_input("Local de destino: ")
                        if dst and src != '':
                            try:
                                shutil.move(f'{"".join(current_path)}/{src}', f'{dst}/{src}')
                            except FileNotFoundError:
                                h.print_error(f"Arquivo/diretório não encontrado.")
                            except PermissionError:
                                h.print_error(f"Permissão negada.")
                            except OSError:
                                h.print_error('Ocorreu um erro.')
                        else:
                            pass
                    elif command_path == '/rename':
                        current_path = remove_last_items(current_path)
                        src = h.ask_input("Nome do arquivo/diretório a renomear: ")
                        dst = h.ask_input("Novo nome: ")
                        try:
                            os.rename(f'{"".join(current_path)}/{src}', f'{"".join(current_path)}/{dst}')
                        except FileNotFoundError:
                            h.print_error(f"Arquivo/diretório não encontrado.")
                        except PermissionError:
                            h.print_error(f"Permissão negada.")
                        except OSError:
                            h.print_error('Ocorreu um erro.')
                    elif command_path == '/h':
                        if getpass.getuser() != 'root':
                            current_path = ['/', '/home', f'/{getpass.getuser()}']
                        else:
                            current_path = ['/', '/root']

                        if is_guest:
                            current_path = ['/', '/home']
                    elif command_path == '/help':
                        h.output("""

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
                    elif command_path == '/l':
                        current_path = remove_last_items(current_path)
                        file_name = h.ask_input("Arquivo: ")
                        try:
                            file_handle = open(f'{"".join(current_path)}/{file_name}', 'r')
                            line_count = 0
                            for line in file_handle.readlines():
                                line_count = line_count + 1
                                h.output(f"{line_count}]", end='', color_code="\033[33m[")
                                h.output(line, end='')
                        except IsADirectoryError:
                            h.print_error('Não é um arquivo.')
                        except PermissionError:
                            h.print_error('Permissão negada.')
                        except UnicodeDecodeError:
                            h.print_error('Apenas arquivos de texto são legiveis!')
                        except FileNotFoundError:
                            h.print_error('Arquivo não encontrado.')
                        except OSError:
                            h.print_error('Ocorreu um erro.')
                    elif command_path == '/*':
                        auto_skip = True
                        current_path = remove_last_items(current_path)
                    elif command_path == '/md':
                        current_path = ['/', '/media', f'/{getpass.getuser()}']
                    elif command_path == '/nada':
                        current_path = remove_last_items(current_path, times=1)
                    elif command_path == '/usrbin':
                        current_path = ['/', '/usr', '/bin']
                    elif command_path == '/texto':
                        current_path = remove_last_items(current_path)
                    elif command_path == '/cln':
                        current_path = remove_last_items(current_path)
                        os.system(h.ask_input("Commando: "))
                    elif command_path == '/bash':
                        current_path = remove_last_items(current_path)
                        os.system("bash")
                    elif command_path == '/search':
                        current_path = remove_last_items(current_path)
                        query = h.ask_input("Procurar arquivs/diretórios que contenham: ")
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
                            h.print_error('Existe um arquivo/diretório com o exato nome digitado.')
                        else:
                            pass
                        if len(matches) > 1:
                            confirm = h.ask_input(f"Deseja exibir todos os \033[35m{len(matches)} \033[32marquivos/diretórios encontrados? ")
                        else:
                            if len(matches) == 1:
                                confirm = h.ask_input(f"Deseja exibir o arquivo/diretório encontrado? ")
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
                                h.output(f'[{num_item}]', end='', color_code="\033[33m")
                            copy_confirm = h.ask_input('Deseja copiar algum nome de arquivo/diretório? ')
                            if copy_confirm in 'Ss' and copy_confirm != '':
                                while True:
                                    try:
                                        clipboard.copy(matches[int(h.ask_input("ID: "))-1])
                                        break
                                    except IndexError:
                                        h.print_error("ID inválido.")
                                    except (TypeError, ValueError):
                                        h.print_error("ID é um número, não outra coisa.")
                                    except KeyError:
                                        h.print_error("Atualmente, essa função não funciona em modo root :/")
                                        break
                    elif command_path == '/i':
                        current_path = remove_last_items(current_path)
                        units = ['byte(s)', 'kilobyte(s)', 'megabyte(s)', 'gigabyte(s)', 'terrabyte(s)', 'petabyte(s)', '']
                        while True:
                            file_name = h.ask_input("Arquivo: ")
                            try:
                                if not os.path.isdir(f"{''.join(current_path)}/{file_name}"):
                                    size = os.stat(f"{''.join(current_path)}/{file_name}").st_size
                                else:
                                    size = get_directory_size(f"{''.join(current_path)}/{file_name}")
                                original_size = size
                                break
                            except FileNotFoundError:
                                h.print_error("Arquivo não encontrado :/")
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
                        h.output(f"""              
    Caminho: {''.join(current_path[1:])}/{file_name}
    Tipo: {mimetypes.guess_type(f'{"".join(current_path)}/{file_name}')[0]}
    Tamanho: {size:.0f} {unit_format} ({original_size} byte(s))
    Criado: {time.ctime(os.path.getctime(f"{''.join(current_path)}/{file_name}"))}
    Modificado: {time.ctime(os.path.getmtime(f"{''.join(current_path)}/{file_name}"))}
                        """, enter_to_continue=True)
                    elif command_path == '/shexec':
                        current_path = remove_last_items(current_path)
                        sudo_confirm = h.ask_input("Sudo? [S/N]")
                        if sudo_confirm in "Ss":
                            run_sudo = 'sudo'
                        else:
                            run_sudo = ''
                        file_name = h.ask_input("Arquivo: ")
                        os.system(f"{run_sudo} sh {''.join(current_path)}/{file_name}")
                    elif command_path == '/full':
                        current_path = remove_last_items(current_path)
                        directory_contents = sorted(os.listdir(f"{''.join(current_path)}"))
                        file_id = -1
                        for item in directory_contents:
                            file_id = file_id + 1
                            h.output(f"[{file_id+1}] {item}")
                    
                    h.wait_for_enter(auto_skip=auto_skip)
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
                    h.print_error(f'Ocorreu um erro! Verifique a ortografia e tente novamente.')
                elif error_type == 'Tipo':
                    h.print_error(f'"{"""""".join(current_path[1:])}/{command_path}" não é um diretório!')
                elif error_type == 'Root':
                    h.print_error(f'Você não tem permissão para acessar "{"""""".join(current_path[1:])}/{command_path}".')
            terminal_size = os.popen('stty size', 'r').read().split()
            terminal_width = int(terminal_size[1])
            continue_flag = True
            # Exibir conteudo do diretório
            if run_count == 1:
                continue_flag = False
            clear_screen()
            if continue_flag:
                h.print_tittle(terminal_width)
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
                h.output('')
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
                        h.output(f"{a:<30}{c:>{terminal_width-20}}")
                        if c == display_items[-1]:
                            break
                    else:
                        h.output(f'{display_items[-1]}')
                        break
                display_metadata = display_items[:]
                display_items = []
                left_index = -1
                right_index = -2
                range_counter = 0
                
    if __name__ == "__main__":
        main()
        
except KeyboardInterrupt:
    print("\n\033[0m")
    h.restore_setterm()
    os.system("clear")
    exit()

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
                    h.output("No momento, copiar como não root não está disponivel.", end='')
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    if not os.path.islink(file_path):
                        if 'kcore' != filename:
                            total_size += os.path.getsize(file_path)
                except FileNotFoundError:
                    pass

        return total_size


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
            except Exception as e:
                h.print_error(e, quit=True)
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
        forbidden_chars = ["*"]
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
                    
                if next_command == '':
                    next_command = '/*'
                    
                next_command = next_command.split('/')
                previous_path = current_path[:]
                for item in next_command:
                    current_path.append(f'/{item}')
                command_path = '/'.join(next_command)
                
                if current_path[0] == '/':
                    auto_skip = False
                    if command_path == '/':
                        try:
                            h.output(', '.join(current_path), enter_to_continue=True)
                            h.remove_last_items(current_path, times=3)
                            auto_skip = True
                        except IndexError:
                            pass
                    elif command_path == '/d':
                        current_path = h.remove_last_items(current_path)
                        n = h.ask_input("Nome do diretório: ")
                        try:
                            os.mkdir(f"{''.join(current_path)}/{n}")
                        except Exception as e:
                            h.print_error(e)
                    elif command_path == '/a':
                        current_path = h.remove_last_items(current_path)
                        n = h.ask_input("Nome do arquivo: ")
                        if n not in directory_contents:
                            try:
                                open(f'{"".join(current_path)}/{n}', 'w+')
                                h.output(f'Arquivo "{n}" criado com sucesso.')
                            except Exception as e:
                                h.print_error(e)
                    elif command_path == '/e':
                        h.output('', end='', color_code="\033[0m")
                        h.restore_setterm()
                        clear_screen()
                        exit()
                    elif command_path == '/del':
                        current_path = h.remove_last_items(current_path)
                        n = h.ask_input("Nome do diretório: ")
                        if n == "/":
                            h.print_error(PermissionError("Nao pode remover o diretório raiz."))
                        else:
                            os.system(f'rm -r "{"""""".join(current_path)}/{n}" >/dev/null 2>&1')
                    elif command_path == '/fdel':
                        current_path = h.remove_last_items(current_path)
                        n = h.ask_input("Nome do arquivo: ")
                        try:
                            os.remove(f"{''.join(current_path)}/{n}")
                        except Exception as e:
                            h.print_error(e)
                        current_path = h.remove_last_items(current_path)
                        current_path = ['/']
                    elif command_path == '/k':
                        current_path = h.remove_last_items(current_path)
                        src = h.ask_input("Nome do arquivo/diretório a copiar: ")
                        dst = h.ask_input("Local a colar: ")

                        # Reescrever essa parte'
                    elif command_path == '/m':
                        current_path = h.remove_last_items(current_path)
                        src = h.ask_input("Nome do arquivo/diretório a mover: ")
                        dst = h.ask_input("Local de destino: ")
                        if dst and src != '':
                            try:
                                shutil.move(f'{"".join(current_path)}/{src}', f'{dst}/{src}')
                            except Exception as e:
                                h.print_error(e)
                        else:
                            pass
                    elif command_path == '/rename':
                        current_path = h.remove_last_items(current_path)
                        src = h.ask_input("Nome do arquivo/diretório a renomear: ")
                        dst = h.ask_input("Novo nome: ")
                        try:
                            os.rename(f'{"".join(current_path)}/{src}', f'{"".join(current_path)}/{dst}')
                        except Exception as e:
                            h.print_error(e)
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
                        current_path = h.remove_last_items(current_path)
                    elif command_path == '/l':
                        current_path = h.remove_last_items(current_path)
                        file_name = h.ask_input("Arquivo: ")
                        try:
                            file_handle = open(f'{"".join(current_path)}/{file_name}', 'rb')
                            line_count = 0
                            for line in file_handle.readlines():
                                line = line.decode('utf-8')
                                line_count = line_count + 1
                                h.output(f"{line_count}]", end='', color_code="\033[33m[")
                                h.output(line, end='')
                        except Exception as e:
                            h.print_error(e)
                    elif command_path == '/*':
                        auto_skip = True
                        current_path = h.remove_last_items(current_path)
                    elif command_path == '/md':
                        current_path = ['/', '/media', f'/{getpass.getuser()}']
                    elif command_path == '/nada':
                        current_path = h.remove_last_items(current_path, times=1)
                    elif command_path == '/usrbin':
                        current_path = ['/', '/usr', '/bin']
                    elif command_path == '/texto':
                        current_path = h.remove_last_items(current_path)
                    elif command_path == '/cln':
                        current_path = h.remove_last_items(current_path)
                        os.system(h.ask_input("Commando: "))
                    elif command_path == '/bash':
                        current_path = h.remove_last_items(current_path)
                        os.system("bash")
                    elif command_path == '/search':
                        pass # Reescrever depois
                    elif command_path == '/i':
                        current_path = h.remove_last_items(current_path)
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
                            except Exception as e:
                                h.print_error(e)
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
                        current_path = h.remove_last_items(current_path)
                        sudo_confirm = h.ask_input("Sudo? [S/N]")
                        if sudo_confirm in "Ss":
                            run_sudo = 'sudo'
                        else:
                            run_sudo = ''
                        file_name = h.ask_input("Arquivo: ")
                        os.system(f"{run_sudo} sh {''.join(current_path)}/{file_name}")
                    elif command_path == '/full':
                        current_path = h.remove_last_items(current_path)
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
                except Exception as e:
                    h.print_error(e)
                    current_path = h.remove_last_items(current_path, times=1)
            run_count = run_count + 1
            text_content = []
            terminal_size = os.popen('stty size', 'r').read().split()
            terminal_width = int(terminal_size[1])
            continue_flag = True
            # Exibir conteudo do diretório
            if run_count == 1:
                continue_flag = False
            clear_screen()
            if continue_flag:
                h.print_tittle(terminal_width)
                h.display_files(directory_contents, current_path, terminal_width, left_index, right_index)
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

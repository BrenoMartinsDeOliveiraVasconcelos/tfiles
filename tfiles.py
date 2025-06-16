#!/usr/bin/env python3
# Caminho e comandos
import os
import getpass
import shutil
import linecache
import readline
import time
import sys
import helpers as h


def main():
    sys.argv.append('')
    
    h.kidnap_current_dir()
    run_count = 0

    complete_path = []
    if sys.argv[1] == '':
        current_path = h.ORIGINAL_DIR.split('/')
    else:
        try:
            current_path = sys.argv[1].split('/')
            os.listdir(f'/{sys.argv[1]}')
        except Exception as e:
            h.print_error(e, quit=True)
    for path_item in current_path:
        complete_path.append(f'/{path_item}')
    current_path = complete_path[:]

    directory_contents = os.listdir(''.join(current_path))
    next_command = ''
    n = ''

    left_index = -1
    right_index = -2

    while True:
        if run_count == 0:
            pass
        else:
            terminal_size = h.get_terminal_size()
            terminal_width = terminal_size[1]
            terminal_height = terminal_size[0]
            h.output('')
            columns = terminal_height
            columns_total = int(columns - (3 + 2 + ((len(directory_contents) / 2) - 0.1)))
            columns_total = columns_total - 1
            auto_skip = False
            remove_times = 1
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
                
                h.clear_screen()
                
            if next_command == '':
                next_command = '/*'
                
            next_command = next_command.split('/')
            for item in next_command:
                current_path.append(f'/{item}')
            command_path = '/'.join(next_command)
            
            if current_path[0] == '/':
                current_path_filesystem = current_path[:-1]
                file_path = f"{''.join(current_path_filesystem)}/{n}"
                if command_path == '/':
                    remove_times = 3
                    auto_skip = True
                elif command_path == '/d':
                    
                    n = h.ask_input("Nome do diretório: ")
                    
                    if os.path.exists(file_path):
                        h.print_error(FileExistsError(f"O diretório '{n}' ja existe."))
                    
                    os.mkdir(file_path)
                elif command_path == '/a':
                    n = h.ask_input("Nome do arquivo: ")
                    if n not in directory_contents:
                        try:
                            open(f'{"".join(current_path_filesystem)}/{n}', 'w+')
                            h.output(f'Arquivo "{n}" criado com sucesso.')
                        except Exception as e:
                            h.print_error(e)
                elif command_path == '/e':
                    return
                elif command_path == '/del':
                    
                    n = h.ask_input("Nome do diretório: ")
                    if n == "/":
                        h.print_error(PermissionError("Nao pode remover o diretório raiz."))
                    else:
                        os.system(f'rm -r "{"""""".join(current_path_filesystem)}/{n}" >/dev/null 2>&1')
                elif command_path == '/fdel':
                    
                    n = h.ask_input("Nome do arquivo: ")
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        h.print_error(e)
                elif command_path == '/k':
                    
                    src = h.ask_input("Nome do arquivo/diretório a copiar: ")
                    dst = h.ask_input("Local a colar: ")

                    # Reescrever essa parte'
                elif command_path == '/m':
                    
                    src = h.ask_input("Nome do arquivo/diretório a mover: ")
                    dst = h.ask_input("Local de destino: ")
                    if dst and src != '':
                        try:
                            shutil.move(f'{"".join(current_path_filesystem)}/{src}', f'{dst}/{src}')
                        except Exception as e:
                            h.print_error(e)
                    else:
                        pass
                elif command_path == '/rename':
                    
                    src = h.ask_input("Nome do arquivo/diretório a renomear: ")
                    dst = h.ask_input("Novo nome: ")
                    try:
                        os.rename(f'{"".join(current_path_filesystem)}/{src}', f'{"".join(current_path_filesystem)}/{dst}')
                    except Exception as e:
                        h.print_error(e)
                elif command_path == '/h':
                    if getpass.getuser() != 'root':
                        current_path = ['/', '/home', f'/{getpass.getuser()}']
                    else:
                        current_path = ['/', '/root']
                        
                        
                    remove_times = 0
                elif command_path == '/help':
                    help_text = open('help.txt', 'r').read()
                    h.output(help_text)
                elif command_path == '/l':
                    
                    file_name = h.ask_input("Arquivo: ")
                    try:
                        file_handle = open(f'{"".join(current_path_filesystem)}/{file_name}', 'rb')
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
                elif command_path == '/usrbin':
                    remove_times = 0
                    current_path = ['/', '/usr', '/bin']
                elif command_path == '/texto':
                    # Reescrever
                    pass
                elif command_path == '/cln':
                    
                    os.system(h.ask_input("Commando: "))
                elif command_path == '/bash':
                    
                    os.system("bash")
                elif command_path == '/search':
                    pass # Reescrever depois
                elif command_path == '/i':
                    
                    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
                    while True:
                        file_name = h.ask_input("Arquivo: ")
                        file = ''.join(h.clear_extra_separatores(current_path_filesystem)[1:]) + '/' + file_name
                        try:
                            size = h.get_size(file)
                            original_size = size
                            break
                        except Exception as e:
                            h.print_error(e)
                    unit_index = 0
                    unit_format = ''
                    while size > 1000:
                        size /= 1000
                        unit_index += 1
                    unit_format = units[unit_index]
                    h.output(f"""              
Caminho: {file}
Tipo: {h.get_mime_type(file)}
Tamanho: {size:.0f} {unit_format} ({original_size} {units[0]})
Criado: {time.ctime(os.path.getctime(file))}
Modificado: {time.ctime(os.path.getmtime(file))}
                    """)
                elif command_path == '/shexec':
                    
                    sudo_confirm = h.ask_input("Sudo? [S/N]")
                    if sudo_confirm in "Ss":
                        run_sudo = 'sudo'
                    else:
                        run_sudo = ''
                    file_name = h.ask_input("Arquivo: ")
                    os.system(f"{run_sudo} sh {''.join(current_path_filesystem)}/{file_name}")
                elif command_path == '/full':
                    directory_contents = sorted(os.listdir(f"{''.join(current_path_filesystem)}"))
                    file_id = -1
                    for item in directory_contents:
                        file_id = file_id + 1
                        h.output(f"[{file_id+1}] {item}")
                else:
                    remove_times = 0
                    auto_skip = True
                current_path = h.remove_last_items(current_path, times=remove_times)
                h.wait_for_enter(auto_skip=auto_skip)
            else:
                current_path = ['/']
            try:
                directory_contents = os.listdir(''.join(current_path))
            except Exception as e:
                h.print_error(e, enter_to_continue=True)
             
            current_path = h.clear_extra_separatores(current_path)   
        run_count = run_count + 1
        continue_flag = True
        # Exibir conteudo do diretório
        if run_count == 1:
            continue_flag = False
        h.clear_screen()
        if continue_flag:
            terminal_height, terminal_width = h.get_terminal_size()
            
            h.print_tittle(terminal_width)
            h.display_files(directory_contents, current_path, terminal_width, left_index, right_index)
            left_index = -1
            right_index = -2
            
if __name__ == "__main__":
    main()
    h.restore_setterm()
    h.clear_screen()
    
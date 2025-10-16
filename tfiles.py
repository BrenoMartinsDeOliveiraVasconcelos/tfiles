#!/usr/bin/env python3
# Caminho e comandos
import os
import getpass
import shutil
import linecache
import readline
import time
import sys
import shlex
import helpers as h
import init

def main():
    sys.argv.append('')
    confirmation_chars = ['S', 'Y', 'y', 's']
    negation_chars = ['N', 'n']
    correct_binaries = confirmation_chars + negation_chars
    
    strings = h.STRINGS
    config = h.CONFIG_FILE
    commands = h.COMMANDS
    
    run_count = 0
    
    if h.is_user_root():
        if not h.ask_yes_no(strings["root_not_recommended"], confirmation_chars, negation_chars):
            sys.exit(0)

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
            print_finished = True
            
            if columns_total > 1:
                h.print_separator(terminal_width)
                for _ in range(1, columns_total):
                    h.output(f"{strings['no_more']:^{terminal_width}}", color_code="\033[1;30m")
            else:
                pass
            if run_count > 1:
                h.switch_emptiness(black=False)
                h.output(" "*terminal_width)
                h.switch_emptiness(black=True)
                h.output(f"\033[1;37m{strings['where_to_go']}")
                h.switch_emptiness(black=True)
                next_command = h.ask_input(f"{strings['path_prompt']}{''.join(current_path[1:])}/ => ")
            else:
                next_command = '/*'
                h.switch_font_blackness(black=False)
                for _ in range(0, 10000):
                    h.output("")
                
                h.clear_screen()
                
            if next_command == '':
                next_command = '/*'

            if next_command == "..":
                next_command = "/" + next_command
                
            next_command = next_command.split('/')
            no_command_current_path = current_path.copy()
            for item in next_command:
                current_path.append(f'/{item}')
            command_path = '/'.join(next_command)
            
            if current_path[0] == '/':
                
                command, args = "", ""

                if len(command_path) > 1:
                    command_path = command_path[1:]
                    command_parsed = shlex.split(command_path)
                    
                    command = command_parsed[0]
                    args = command_parsed[1:]

                    command_list = [x[0][1:] for x in commands]
                    arg_list = [x[1] for x in commands]

                    if command in command_list:
                        num_args = arg_list[command_list.index(command)]

                        if len(args) < num_args:
                            h.output(strings['not_enough_arguments'] % num_args, enter_to_continue=True)
                            command = "*"
                        else:
                            remove_times += "".join(args).count('/')

                            index = 0
                            for _ in args:
                                if not args[index].startswith('/'):
                                    args[index] = h.join_path(no_command_current_path, args[index])
                                index += 1
                
                if command == "..":
                    remove_times = 3
                    auto_skip = True
                    print_finished = False
                elif command == 'd':
                    n = args[0]
                    if os.path.exists(n):
                        error_msg = strings['directory_exists_error'] % n
                        h.print_error(FileExistsError(error_msg))
                    
                    os.mkdir(n)
                elif command == 'a':
                    file = args[0]
                    print(file)
                    try:
                        if os.path.exists(file):
                            raise FileExistsError(strings['file_exists_error'] % file)
                        else:
                            open(file, 'w+').close()
                            h.output(strings['file_created_success'] % file)
                    except Exception as e:
                        h.print_error(e)
                elif command == 'e':
                    return
                elif command == 'del':
                    n = args[0]
                    if n == "/":
                        h.print_error(PermissionError(strings['cannot_remove_root']))
                    else:
                        
                        if not os.path.exists(n):
                            h.print_error(FileNotFoundError(strings['file_not_found_error'] % n))
                        
                        if os.path.isfile(n):
                            os.remove(n)
                        else:
                            os.system(f'rm -r "{n}" >/dev/null 2>&1')
                elif command == 'k':
                    src = args[0]
                    dst = args[1]

                    try:
                        if os.path.isfile(src):
                            shutil.copy2(src, dst)
                        else:
                            shutil.copytree(src, dst)
                            
                        h.output(strings['copied_success'])
                    except Exception as e:
                        h.print_error(e)
                elif command == 'm':
                    src = args[0]
                    dst = args[1]
                    if dst and src != '':
                        try:
                            print(src, dst)
                            shutil.move(src, dst)
                        except Exception as e:
                            h.print_error(e)
                    else:
                        pass
                elif command == 'rename':
                    src = args[0]
                    dst = args[1]
                    try:
                        os.rename(src, dst)
                    except Exception as e:
                        h.print_error(e)
                elif command == 'h':
                    if getpass.getuser() != 'root':
                        current_path = ['/', '/home', f'/{getpass.getuser()}']
                    else:
                        current_path = ['/', '/root']
                        
                    remove_times = 0
                elif command == 'help':
                    h.print_help()
                elif command == 'read':
                    file_name = args[0]
                    try:
                        h.print_text(file_name, negation_chars)
                    except Exception as e:
                        h.print_error(e)
                elif command in ['*', '.'] or command_path == "/":
                    auto_skip = True
                elif command == 'usrbin':
                    remove_times = 0
                    current_path = ['/', '/usr', '/bin']
                elif command == 'text':
                    enviroment = os.environ
                    default_editor = ""
                    
                    file_path = args[0]
                    
                    for key in enviroment.keys():
                        if key == 'EDITOR':
                            default_editor = enviroment[key]
                            break
                    if default_editor == "":
                        h.output(strings['editor_not_found'])
                    elif os.path.exists(file_path):
                        if os.path.isfile(file_path):
                            os.system(f"{default_editor} {file_path}")
                        else:
                            h.output(strings['is_not_file'])
                    else:
                        h.output(strings['file_not_found'])
                    
                elif command == 'cln':
                    os.system(h.ask_input(strings['command_prompt']))
                elif command == 'bash':
                    os.system("bash")
                elif command == 'search':
                    answ = h.ask_yes_no(strings['search_prompt'], confirmation_chars, negation_chars)
                    search_location =  ''.join(no_command_current_path)
                        
                    name = h.ask_input(strings['search_name'])     
                        
                    if answ:
                        search_location = "/"
                    
                    founds = []
                    start_time = time.time()
                    for root, _, files in os.walk(search_location):
                        for file in files:
                            h.print_wait_time(start_time)        
                            if name in file:
                                founds.append(os.path.join(root, file))
                    
                    number_found = len(founds)  
                    if number_found == 0:
                        h.output(strings['search_not_found'])
                    else:
                        h.output(strings['search_found'] % number_found)
                        h.print_calmly(founds, negation_chars)
                        
                        output_select = h.input_index(founds)
                        
                        if output_select is not None:
                            current_path = output_select
                elif command == 'i':
                    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
                    while True:
                        file = args[0]
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

                    if os.path.exists(file):
                        unit_format = units[unit_index]
                        output_list = [
                            f"{strings['info_path']}{file}",
                            f"{strings['info_type']}{h.get_mime_type(file)}",
                            f"{strings['info_size']}{size:.0f} {unit_format} ({original_size} {units[0]})",
                            f"{strings['info_created']}{time.ctime(os.path.getctime(file))}",
                            f"{strings['info_modified']}{time.ctime(os.path.getmtime(file))}"
                        ]
                        for stdout in output_list:
                            h.output(stdout)
                    else:
                        h.print_error(FileNotFoundError(" "))
                elif command == 'shexec':
                    sudo_confirm = h.ask_input(strings['sudo_prompt'])
                    if sudo_confirm in confirmation_chars:
                        run_sudo = 'sudo'
                    else:
                        run_sudo = ''
                    file_name = args[0]
                    os.system(f"{run_sudo} sh {file_name}")
                elif command == 'full':
                    directory_contents = sorted(os.listdir(f"{''.join(no_command_current_path)}"))
                    file_id = -1
                    for item in directory_contents:
                        file_id = file_id + 1
                        h.output(f"[{file_id+1}] {item}")
                elif command == 'about':
                    about = config["about"]
                    strings_output = [f"{about["program"]}", f"v{about['version']}",
                                      "-", f"{about['developer']}", f"({about['year'][0]}-{about['year'][1]})"]
                    
                    h.output(" ".join(strings_output))
                elif command == 'cd':
                    n = args[0]
                        
                    if os.path.exists(n):
                        current_path = ["/"+x for x in n.split('/')]
                        remove_times = 0
                    else:
                        h.output(strings['path_not_found'])
                    
                elif command == "deep_search":
                    search_on_fs = h.ask_yes_no(strings['search_prompt'], confirmation_chars, negation_chars)
                        
                    text_look = h.ask_input(strings['deep_search_name'])
                    
                    search_path = "/" if search_on_fs else ''.join(no_command_current_path)

                    founds = []
                    start_time = time.time()
                    blacklist = ["/dev", "/sys", "/proc", "/boot", "/run"]
                    for root, _, files in os.walk(search_path):
                        skip = False
                        
                        for path in blacklist:
                            if root.startswith(path):
                                skip = True
                                break
                        if skip:
                            continue
                        
                        for file in files:
                            try:
                                h.print_wait_time(start_time, interval=0.01)
                                file_content = open(os.path.join(root, file), 'rb').read().decode('utf-8')
                                
                                if text_look in file_content:
                                    founds.append(os.path.join(root, file))
                            except Exception as e:
                                pass
                            
                    number_found = len(founds)
                    if number_found == 0:
                        h.output(strings['search_not_found'])
                    else:
                        h.output(strings['search_found'] % number_found)
                        h.print_calmly(founds, negation_chars)
                        
                        output_select = h.input_index(founds)
                        
                        if output_select is not None:
                            current_path = output_select
                else:
                    remove_times = 0 if command != '' else 1
                    auto_skip = True
                    print_finished = False
                current_path = h.remove_last_items(current_path, times=remove_times)
                
                if print_finished:
                    h.output(strings['finished'])
                
                h.wait_for_enter(auto_skip=auto_skip)
            else:
                current_path = ['/']
            try:
                directory_contents = os.listdir(''.join(current_path))
            except Exception as e:
                h.print_error(e, enter_to_continue=True)
                current_path = h.remove_last_items(current_path, times=1)
             
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
    h.kidnap_current_dir()
    init_functions = [init.set_language, init.restore_config]
    
    restart = False
    
    for init_function in init_functions:
        restart = init_function()
        if restart:
            break
    
    if not restart:
        main()
        h.restore_setterm()
        h.clear_screen()
    else:
        h.free_current_dir()
        os.system(f"{h.SCRIPT_DIR}/run.sh")
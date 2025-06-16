import os
import getpass
import mimetypes

ORIGINAL_DIR = os.getcwd()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_mime_type(file_path):
    mime = mimetypes.guess_type(file_path)[0]
    
    if mime is None:
        return 'directory'
    else:
        return mime


def wait_for_enter(auto_skip=False):
        if not auto_skip:
            ask_input("Enter para continuar.")

def print_error(error: Exception, enter_to_continue: bool=False, quit: bool=False) -> None:
    message = ""
    
    if isinstance(error, FileNotFoundError):
        message = "O arquivo especificado não foi encontrado."
    elif isinstance(error, PermissionError):
        message = "Permissão negada. Tente novamente como root."
    elif isinstance(error, NotADirectoryError):
        message = "O diretório especificado não é um diretório."
    elif isinstance(error, FileExistsError):
        message = "O arquivo ou diretório especificado ja existe."
    elif isinstance(error, OSError):
        message = "Erro de sistema: " + str(error)
    elif isinstance(error, IsADirectoryError):
        message = "O arquivo especificado é um diretório."
    elif isinstance(error, UnicodeDecodeError):
        message = "Erro ao decodificar o arquivo."
    elif isinstance(error, UnicodeEncodeError):
        message = "Erro ao codificar o arquivo."
    elif isinstance(error, KeyboardInterrupt):
        message = "Operação cancelada pelo usuário."
    else:
        message = "Erro desconhecido: " + str(error)
    
    
    print("\033[1;31m" + message + "\033[37m")
    
    if enter_to_continue:
        wait_for_enter()
        
    if quit:
        exit(1)

    
def ask_input(message):    
    return input("\033[37m" + message + "\033[37m")


def output(message, color_code="\033[37m", end='\n', enter_to_continue=False):
    print(color_code + message + "\033[37m", end=end)
    
    if enter_to_continue:
        wait_for_enter()


def print_tittle(terminal_width):
        os.system('setterm -background white -foreground white')
        text = "Terminal Explorer"
        if getpass.getuser() == 'root':
            text += " (ROOT)"
        
        output(f"{f'{text}':^{terminal_width}}", color_code="\033[1;30m")
        os.system('setterm -background black foreground black')
        

def print_separator(terminal_width):
        os.system('setterm -background white -foreground white')
        columns_text = f''
        output(f"{columns_text}", color_code="\033[1;30m", end='')
        output(' '* int(terminal_width - len(columns_text)))
        os.system('setterm -background black -foreground black')
        
        
def switch_emptiness(black: bool):
    color = 'black' if black else 'white'
    
    os.system(f"setterm -background {color} -foreground {color}")
    

def switch_font_blackness(black: bool):
    background = 'black' if not black else 'white'
    foregound = 'black' if black else 'white'
    
    os.system(f"setterm -background {background} -foreground {foregound}")


def restore_setterm():
    print("\n\033[0m")
    os.system('setterm -default')


def display_files(directory_contents: list, current_path: list, terminal_width: int, left_index: int, right_index: int):
    display_items = []
    new_loop = []
    temp_display = []
    range_counter = ""
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
            if 'text' in file_type[0]: # type: ignore
                temp_display.append('\033[35m[•]')
            elif 'application' in file_type[0]: # type: ignore
                temp_display.append("\033[36m[>]")
            elif 'audio' in file_type[0]: # type: ignore
                temp_display.append('\033[33m[𝄞]')
            elif 'video' in file_type[0]: # type: ignore
                temp_display.append('\033[30m[▶]')
            elif 'image' in file_type[0]: # type: ignore
                temp_display.append("\033[33m[☀]")
            elif 'font' in file_type[0]: # type: ignore
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
    display_items_size = len(display_items)
    for index in range(0, display_items_size):
        left_index = left_index + 2
        right_index = right_index + 2
        break_loop = False
        if display_items_size > 1:
            try:
                a = display_items[right_index]
            except IndexError:
                range_counter = 'end'
            try:
                c = display_items[left_index]
            except IndexError:
                range_counter = 'end'
        elif display_items_size== 1:
            a = ''.join(display_items)
            c = ''
        else:
            a = 'Diretório vazio :/'
            c = ''
        
        if range_counter != 'end' or c == display_items[-1]:
            end_c = '\n'
            
            if c == display_items[-1]:
                end_c = ''
                break_loop = True
            
            output(f"{a:<30}", end='')
            output(f"{c:>{terminal_width-20}}", end=end_c)
        else:
            output(f'{display_items[-1]}', end="")
            break_loop = True
            
        if break_loop:
            break
        

def remove_last_items(item_list: list, times: int=2) -> list:
    for _ in range(0, times):
        item_list.pop()
        
        if len(item_list) == 1:
            break

    return item_list


def clear_screen():
    os.system("clear")


def clear_extra_separatores(item_list: list) -> list:
    fixed_list = []
    
    if len(item_list) <= 1:
        return item_list
    
    index = 0
    for item in item_list:
        if item != '/':
            fixed_list.append(item)
        else:
            if index == 0:
                fixed_list.append(item)
            
        index += 1
    
    return fixed_list


def get_size(start_path = '.') -> int:
    
    if os.path.isfile(start_path):
        return os.path.getsize(start_path)
    
    count = 0
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        dirnames = dirnames
        count = count + 1
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                if not os.path.islink(file_path):
                    if 'kcore' != filename:
                        total_size += os.path.getsize(file_path)
            except FileNotFoundError:
                pass

    return total_size


def get_terminal_size() -> tuple[int, int]:
        terminal_size = os.popen('stty size', 'r').read().split()
        terminal_width = int(terminal_size[1])
        terminal_height = int(terminal_size[0])
        
        return terminal_height, terminal_width
    
    
def kidnap_current_dir():
    os.chdir(SCRIPT_DIR)
    

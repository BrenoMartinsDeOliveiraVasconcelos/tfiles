import os
import getpass
import mimetypes
import json
import time
import datetime

TRANSLATION_FOLDER = "translations"
HELP_FOLDER = "help"
STRINGS_FOLDER = "strings"

CONFIG_FILE = json.load(open('config.json'))
LANG = CONFIG_FILE['language']
STRINGS = json.load(open(os.path.join(TRANSLATION_FOLDER, STRINGS_FOLDER, f'{LANG}.json')))
HELP = json.load(open(os.path.join(TRANSLATION_FOLDER, HELP_FOLDER, f'{LANG}.json'))) # type: dict
SYMBOLS = CONFIG_FILE['symbols']
COMMANDS = CONFIG_FILE['commands']

ORIGINAL_DIR = os.getcwd()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_mime_type(file_path):
    
    mime_raw = mimetypes.guess_type(file_path)
    
    mime = mime_raw[0]
    
    if mime is None:
        if os.path.isdir(file_path):
            mime = 'directory'
        elif os.path.isfile(file_path):
            mime = 'binary'
        else:
            mime = 'unknown'
            
            
    return mime.split('/')[0]


def wait_for_enter(auto_skip=False):
        if not auto_skip:
            ask_input(STRINGS['enter_to_continue'])


def print_error(error: Exception, enter_to_continue: bool=False, quit: bool=False) -> None:
    message = ""
    
    if isinstance(error, FileNotFoundError):
        message = STRINGS['file_not_found']
    elif isinstance(error, PermissionError):
        message = STRINGS['permission_denied']
    elif isinstance(error, NotADirectoryError):
        message = STRINGS['not_a_directory']
    elif isinstance(error, FileExistsError):
        message = STRINGS['file_exists']
    elif isinstance(error, OSError):
        message = STRINGS['os_error'] + str(error)
    elif isinstance(error, IsADirectoryError):
        message = STRINGS['is_a_directory']
    elif isinstance(error, UnicodeDecodeError):
        message = STRINGS['unicode_decode_error']
    elif isinstance(error, UnicodeEncodeError):
        message = STRINGS['unicode_encode_error']
    elif isinstance(error, KeyboardInterrupt):
        message = STRINGS['keyboard_interrupt']
    else:
        message = STRINGS['unknown_error'] + str(error)
    
    
    print("\033[1;31m" + message + "\033[37m")
    
    if enter_to_continue:
        wait_for_enter()
        
    if quit:
        exit(1)

    
def ask_input(message):    
    user_input = input("\033[37m" + message + "\033[37m")
        
    return user_input


def output(message, color_code="\033[37m", end='\n', enter_to_continue=False, flush=True):
    
    print(color_code + message + "\033[37m", end=end, flush=flush)
    
    if enter_to_continue:
        wait_for_enter()


def print_tittle(terminal_width):
        os.system('setterm -background white -foreground white')
        text = STRINGS['terminal_explorer']
        if getpass.getuser() == 'root':
            text += STRINGS['root_indicator']
        
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
        file_type = get_mime_type(join_path(current_path, item))
        mime_symbol = SYMBOLS['mimes'][file_type]
        temp_display.append(f"\033[{mime_symbol[1]}m[{mime_symbol[0]}]")
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
        elif display_items_size == 1:
            a = ''.join(display_items)
            c = ''
        else:
            a = STRINGS['empty_directory']
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
    start_time = time.time()
    output("")
    for dirpath, dirnames, filenames in os.walk(start_path):
        dirnames = dirnames
        count = count + 1
        for filename in filenames:
            print_wait_time(start_time)
            file_path = os.path.join(dirpath, filename)
            
            if not os.path.exists(file_path):
                continue
            
            if not os.path.islink(file_path):
                if 'kcore' != filename:
                    total_size += os.path.getsize(file_path)
    output("")
    return total_size


def get_terminal_size() -> tuple[int, int]:
        terminal_size = os.popen('stty size', 'r').read().split()
        terminal_width = int(terminal_size[1])
        terminal_height = int(terminal_size[0])
        
        return terminal_height, terminal_width
    
    
def kidnap_current_dir():
    os.chdir(SCRIPT_DIR)


def join_path(path: list, include: str) -> str:
    return '/'.join(path + [include])


def is_number(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def print_calmly(array: list, negation_chars: list):
    index = 0
    output(STRINGS["negate_to_cancel"])
    for item in array:
        index += 1
        output(f"[{index}] {item}", end="")
        
        answer_continue = "\0"
        while answer_continue == "\0":
            answer_continue = ask_input('')
            
        break_it = answer_continue in negation_chars
        if break_it:
            break


def print_help():
    for key, value in HELP.items():
        if key == "symbols":
            output(f"\n{value['name']}\n")
            values_mimes = [value for _, value in SYMBOLS["mimes"].items()] #list
            icons = [x[0] for x in values_mimes] # type: list 
            colors = [x[1] for x in values_mimes] # type: list
            index = 0
            for x in value['lines']:
                output(f"[{icons[index]}]", end="", color_code=f"\033[{colors[index]}m")
                output(f" {x}")
                index += 1
        elif key == "commands":
            output(f"\n{value['name']}\n")
            index = 0
            for x in value["lines"]:
                output(f"{COMMANDS[index]} - {x}")
                index += 1
                

def print_wait_time(start_time: float, interval: float = 0.05):
    unit = 10**6
    interval *= unit
    start_time *= unit
    current_time = time.time() * unit

    time_diff = current_time - start_time  
    
    if time_diff % interval == 0:
        output(STRINGS['work_in_progress'] % (time_diff / unit))



def print_text(path: str, negation_chars: list):
    print(path)
    file = open(path, 'rb')
    text = file.read().decode('utf-8').split('\n')
    
    print_calmly(text, negation_chars)
import os
import getpass

def wait_for_enter(auto_skip=False):
        if not auto_skip:
            ask_input("Enter para continuar.")

def print_error(message, enter_to_continue=False, quit=False):
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
    os.system('setterm -default')
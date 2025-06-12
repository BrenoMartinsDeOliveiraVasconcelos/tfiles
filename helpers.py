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
        
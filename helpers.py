def print_error(message):
    print("\033[1;31m" + message + "\033[37m")
    
    
def ask_input(message):
    return input("\033[37m" + message + "\033[37m")
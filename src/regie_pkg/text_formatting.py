"""module to format string"""

def bold(str_val: str) -> str:
    '''bold string format'''
    return f"\033[1m{str_val}\033[0m"

def underline(str_val: str) -> str:
    '''underline string format'''
    return f"\033[4m{str_val}"

def add_newline(str_val: str) -> str:
    '''adds newline char'''
    return str_val + "\n"



def insert_newline(num_of_lines=1) -> None:
    for _ in range(num_of_lines):
        print()
    return 
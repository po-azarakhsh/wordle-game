from termcolor import colored

def print_success(text, end=' '):
    print(colored(text, 'green', attrs=['reverse']), end=end)

def print_warning(text, end=' '):
    print(colored(text, 'yellow', attrs=['reverse']), end=end)

def print_wrong(text, end=' '):
    print(colored(text, 'grey', attrs=['reverse']), end=end)

def print_error(text, end=' '):
    print(colored(text, 'red', attrs=['reverse']), end=end)

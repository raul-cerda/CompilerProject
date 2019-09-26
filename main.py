# Raul Cerda
# April 24, 2019
import queue


TOKEN_LIST = queue.Queue()
CURRENT_TOKEN = ['sigma', 'none']
OUTPUT_FILE = open("output.txt", "w+")
PRODUCTION_RULES = ['S -> i = E', 'E -> TQ', 'Q -> +TQ', 'Q -> -TQ', 'Q -> sigma', 'T -> FR', 'R -> *FR', 'R -> /FR',
                    'R -> sigma', 'F -> (E)', 'F -> i']
# if, while, and declaration expand S so that S -> i=E | if(E){E} | while(E){E} | int i = i | bool i = TorF
# else addition adds rule S -> if(E){E}else{E}


def main():
    get_all_tokens()
    while not TOKEN_LIST.empty():
        S()
    OUTPUT_FILE.close()


def get_next_token():
    global CURRENT_TOKEN
    if TOKEN_LIST.empty():
        exit()
    if CURRENT_TOKEN[0] == 'sigma':
        CURRENT_TOKEN = TOKEN_LIST.get()
        OUTPUT_FILE.write(CURRENT_TOKEN[0] + ": " + CURRENT_TOKEN[1] + '\n')
    return CURRENT_TOKEN


def S():
    global CURRENT_TOKEN
    token = get_next_token()

    if token[1] == 'if' or token[1] == 'while':
        CURRENT_TOKEN = ['sigma', 'none']
        token = get_next_token()
        if token[1] == '(':
            CURRENT_TOKEN = ['sigma', 'none']
            S()
            token = get_next_token()
            if token[1] == ')':
                CURRENT_TOKEN = ['sigma', 'none']
                token = get_next_token()
                if token[1] == '{':
                    CURRENT_TOKEN = ['sigma', 'none']
                    S()
                    token = get_next_token()
                    if token[1] != '}':
                        print("Error: Expected '}' (Rule S)")
                        exit()
                    else:
                        CURRENT_TOKEN = ['sigma', 'none']
                        token = get_next_token()
                        if token[1] == 'else':
                            CURRENT_TOKEN = ['sigma', 'none']
                            token = get_next_token()
                            if token[1] == '{':
                                CURRENT_TOKEN = ['sigma', 'none']
                                S()
                                token = get_next_token()
                                if token[1] != '}':
                                    print("Error: Expected '}' for Else Block (Rule S)")
                                    exit()
                                else:
                                    CURRENT_TOKEN = ['sigma', 'none']
                else:
                    print("Error: Expected '{' (Rule S)")
                    exit()
            else:
                print("Error: Expected ')' (Rule S)")
                exit()
        else:
            print("Error: Expected '(' (Rule S)")
            exit()
    elif token[1] == 'int':
        CURRENT_TOKEN = ['sigma', 'none']
        token = get_next_token()
        if token[0] == 'identifier':
            CURRENT_TOKEN = ['sigma', 'none']
            token = get_next_token()
            if token[1] == '=':
                CURRENT_TOKEN = ['sigma', 'none']
                token = get_next_token()
                if token[0] != 'identifier':
                    print("Error: Expected value for int declaration")
                    exit()
                else:
                    CURRENT_TOKEN = ['sigma', 'none']
            else:
                print("Error: Expected '=' for declaration")
                exit()
        else:
            print("Error: Expected variable name for int declaration")
    elif token[1] == 'bool':
        CURRENT_TOKEN = ['sigma', 'none']
        token = get_next_token()
        if token[0] == 'identifier':
            CURRENT_TOKEN = ['sigma', 'none']
            token = get_next_token()
            if token[1] == '=':
                CURRENT_TOKEN = ['sigma', 'none']
                token = get_next_token()
                if token[1] != 'T' and token[1] != 'F':
                    print("Error: Expected 'T' or 'F' for bool declaration")
                    exit()
                else:
                    CURRENT_TOKEN = ['sigma', 'none']
            else:
                print("Error: Expected '=' for bool declaration")
                exit()
        else:
            print("Error: Expected variable name for bool declaration")
    elif token[0] == 'identifier':
        OUTPUT_FILE.write(PRODUCTION_RULES[0] + '\n')
        CURRENT_TOKEN = ['sigma', 'none']
        token = get_next_token()
        if token[0] == "equal":
            CURRENT_TOKEN = ['sigma', 'none']
            E()
        else:
            print("Error: Expected '=' (Rule S)")
            exit()
    else:
        print("Error: Expected identifier, if, while, or int/bool type for declaration (Rule S)")
        exit()


def E():
    T()
    OUTPUT_FILE.write(PRODUCTION_RULES[1] + '\n')
    Q()


def Q():
    global CURRENT_TOKEN
    token = get_next_token()
    if token[0] == "plus" or token[0] == "minus":
        if token[0] == "plus":
            OUTPUT_FILE.write(PRODUCTION_RULES[2] + '\n')
        else:
            OUTPUT_FILE.write(PRODUCTION_RULES[3] + '\n')
        CURRENT_TOKEN = ['sigma', 'none']
        T()
        Q()
    else:
        OUTPUT_FILE.write(PRODUCTION_RULES[4] + '\n')
        return


def T():
    F()
    OUTPUT_FILE.write(PRODUCTION_RULES[5] + '\n')
    R()


def R():
    global CURRENT_TOKEN
    token = get_next_token()
    if token[0] == 'star' or token[0] == 'slash':
        if token[0] == 'star':
            OUTPUT_FILE.write(PRODUCTION_RULES[6] + '\n')
        else:
            OUTPUT_FILE.write(PRODUCTION_RULES[7] + '\n')
        CURRENT_TOKEN = ['sigma', 'none']
        F()
        R()
    else:
        OUTPUT_FILE.write(PRODUCTION_RULES[8] + '\n')
        return


def F():
    global CURRENT_TOKEN
    token = get_next_token()
    if token[0] == "l_parenthesis":
        OUTPUT_FILE.write(PRODUCTION_RULES[9] + '\n')
        CURRENT_TOKEN = ['sigma', 'none']
        E()
        token = get_next_token()
        if token[0] != 'r_parenthesis':
            print('Error: Expected right parenthesis (Rule F)')
            exit()
        CURRENT_TOKEN = ['sigma', 'none']
    elif token[0] == 'identifier':
        OUTPUT_FILE.write(PRODUCTION_RULES[10] + '\n')
        CURRENT_TOKEN = ['sigma', 'none']
        return
    else:
        print('Error: Expected left parenthesis (Rule F)')
        exit()


# lexical analysis portion
# state values
# 1 = init    2 = word    3 = num    4 = num w/decimal
# 5 = separator    6 = operator    7 = identifier    8 = int    9 = real    10 = comment to ignore

# State 10 is a temp state that detects the initial ! mark and transitions to state 11
# State 11 keeps checking for end comment mark and returns to initial state when ! detected


def get_all_tokens():
    # keywords = ['int', 'float', 'bool', 'if', 'else', 'then', 'do', 'while', 'whileend', 'do', 'doend', 'for',
                # 'and', 'or', 'function']
    separators = ['\'', '(', ')', '{', '}', '[', ']', ',', '.', ':', ';', '!', ' ', '\n']
    operators = ['*', '+', '-', '=', '/', '>', '<', '%']

    state = 1
    state_to_be = 1
    current_str = ''
    input_file = open("input.txt", "r")
    for line in input_file:
        for c in line:
            if state == 1:
                if c.isalpha():
                    state = 2
                    current_str = current_str + c
                elif c.isnumeric():
                    state = 3
                    current_str = current_str + c
                elif c in separators:
                    if c == '!':
                        state = 10
                    else:
                        state = 5
                elif c in operators:
                    state = 6
            elif state == 2:
                if c.isalnum() or c == '$':
                    state = 2
                    current_str = current_str + c
                elif c in separators:
                    state = 7
                    if c == '!':
                        state_to_be = 10
                    else:
                        state_to_be = 5
                elif c in operators:
                    state = 7
                    state_to_be = 6
            elif state == 3:
                if c.isnumeric():
                    state = 3
                    current_str = current_str + c
                elif c == '.':
                    state = 4
                    current_str = current_str + c
                elif c.isalpha():
                    state = 8
                    state_to_be = 2
                elif c in separators:
                    state = 8
                    if c == '!':
                        state_to_be = 10
                    else:
                        state_to_be = 5
                elif c in operators:
                    state = 8
                    state_to_be = 6
            elif state == 4:
                if c.isnumeric():
                    state = 4
                    current_str = current_str + c
                elif c.isalpha():
                    state = 9
                    state_to_be = 2
                elif c in separators:
                    state = 9
                    if c == '!':
                        state_to_be = 10
                    else:
                        state_to_be = 5
                elif c in operators:
                    state = 9
                    state_to_be = 6
            if state == 7:
                TOKEN_LIST.put(['identifier', current_str])
                state = state_to_be
            if state == 8:
                TOKEN_LIST.put(['identifier', current_str])
                state = state_to_be
                current_str = c
            if state == 9:
                TOKEN_LIST.put(['identifier', current_str])
                state = state_to_be
                current_str = c
            if state == 5:
                if c != ' ' and c != '\n':
                    if c == '(':
                        TOKEN_LIST.put(['l_parenthesis', c])
                    elif c == ')':
                        TOKEN_LIST.put(['r_parenthesis', c])
                    elif c == '{':
                        TOKEN_LIST.put(['l_curly', c])
                    elif c == '}':
                        TOKEN_LIST.put(['r_curly', c])
                state = 1
                current_str = ''
            if state == 6:
                if c == '+':
                    TOKEN_LIST.put(['plus', c])
                elif c == '-':
                    TOKEN_LIST.put(['minus', c])
                elif c == '*':
                    TOKEN_LIST.put(['star', c])
                elif c == '/':
                    TOKEN_LIST.put(['slash', c])
                elif c == '=':
                    TOKEN_LIST.put(['equal', c])
                state = 1
                current_str = ''
            if state == 11:
                if c == '!':
                    state = 1
            if state == 10:
                state = 11

    if state == 2:
        TOKEN_LIST.put(['identifier', current_str])
    elif state == 3:
        TOKEN_LIST.put(['identifier', current_str])
    elif state == 4:
        TOKEN_LIST.put(['identifier', current_str])


main()

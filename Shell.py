import os
import sys
import re

def change_directory(user_input_array):
    try:
        os.chdir(user_input_array[1])
    except FileNotFoundError:
        pass

def list_directory(user_input_array):
    # print("files and directories in ", os.listdir("/"))
    try:
        if user_input_array[1] == ">":
            path = user_input_array[2]
    except IndexError:
        path = os.getcwd()
        pass
    dirs = os.listdir(path)
    for file in dirs:
        print(file)

def redirection(user_input_array):
    if '>'in user_input_array:
        os.close(1)
        os.open(user_input_array[user_input_array.index('>')+1],os.O_CREAT | os.O_WRONLY) # if it doesn't exsists then create if it exsists then only write
        os.set_inheritable(1, True) # honestly don't know what this does but all the tutorials have this
        do_Commands(user_input_array[0:user_input_array.index('>')])
    else:
        os.close(0)
        os.open(user_input_array[user_input_array.index('<')+1], os.O_RDONLY)
        do_Commands(user_input_array[0:user_input_array.index('<')])

def do_Commands(user_input_array):
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir, user_input_array[0])
        try:
            os.execve(program, user_input_array, os.environ)
        except FileNotFoundError:
            pass
    os.write(2, ("Error: Command:'%s' not found." % user_input_array[0]).encode())
    sys.exit(1)
while True:
    # requirement 1 make $ as ps1
    if 'PS1' not in os.environ:
        p = os.getcwd() + ' $'
        os.write(1, p.encode())
    else:
        os.environ['PS1']
    try:
        user_input_string = input().strip()
        user_input_array = user_input_string.split()
    except EOFError:
        sys.exit(1)
    # user_input = input()
    # print("command: ", user_input_string)
    # requirement 4 part a exit
    if "exit" in user_input_array:
        sys.exit(0)
    # requirement 4 part b change directory
    elif "cd" in user_input_array[0]:
        change_directory(user_input_array)

    elif '>' in user_input_array or '<' in user_input_array:
        redirection(user_input_array)

    else:
        print(user_input_string, ": command not found")

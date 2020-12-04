import os
import re
import sys


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
    if '>' in user_input_array:
        os.close(1)
        os.open(user_input_array[user_input_array.index('>') + 1],
                os.O_CREAT | os.O_WRONLY)  # if it doesn't exsists then create if it exsists then only write
        os.set_inheritable(1, True)  # honestly don't know what this does but all the tutorials have this
        do_commands(user_input_array[0:user_input_array.index('>')])
    else:
        os.close(0)
        os.open(user_input_array[user_input_array.index('<') + 1], os.O_RDONLY)
        do_commands(user_input_array[0:user_input_array.index('<')])


def do_commands(user_input_array):
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir, user_input_array[0])
        try:
            os.execve(program, user_input_array, os.environ)
        except FileNotFoundError:
            pass
    os.write(2, ("Error: Command:'%s' not found." % user_input_array[0]).encode())
    sys.exit(1)


def pipe_work(user_input_array):
    read_side = user_input_array[user_input_array.index('|') + 1:]
    write_side = user_input_array[0:user_input_array.index('|')]
    piper, pipew = os.pipe()
    for f in (piper, pipew):
        os.set_inheritable(f, True)
    pipe_rc = os.fork()
    if pipe_rc == 0:
        os.close(1)
        os.dup(pipew)
        os.set_inheritable(1, True)
        for fd in (piper, pipew):
            os.close(fd)
        do_commands(write_side)
        sys.exit(1)
    elif pipe_rc > 0:
        os.close(0)
        os.dup(piper)
        os.set_inheritable(0, True)
        for fd in (piper, pipew):
            os.close(fd)
        if "|" in read_side:  # more than one |
            pipe_work(read_side)
        do_commands(read_side)
    else:
        os.write(2, ('Fork fail').encode())
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
    if "exit" in user_input_array:
        sys.exit(0)
    job_control_sign = False if '&' in user_input_array else True
    if not job_control_sign:
        user_input_array.remove('&')
    if len(user_input_array) <= 0:
        continue
    # requirement 4 part b change directory
    if "cd" in user_input_array[0]:
        change_directory(user_input_array)

    elif "|" in user_input_array:
        # hey its a pipe
        pipe_work(user_input_array)

    elif '>' in user_input_array or '<' in user_input_array or '/' in user_input_array or ':' in user_input_array:
        race_condition = os.fork()
        if race_condition < 0:
            os.write(2, ("Fork Fail" % race_condition).encode())
            sys.exit(1)
        elif race_condition == 0:
            if '/' in user_input_array[0]:
                try:
                    os.execve(user_input_array[0],user_input_array,os.environ)
                except FileNotFoundError:
                    pass
            elif '>' in user_input_array or '<' in user_input_array:  # redirect
                redirection(user_input_array)
            elif ':' in user_input_array:
                for dire in re.split(":", os.environ['PATH']):
                    program = "%s/%s" % (dire, user_input_array[0])
                try:
                    os.execve(program, user_input_array, os.environ)
                except FileNotFoundError:
                    pass
        else:
            if job_control_sign:
                os.wait()
    else:
        print(user_input_string, ": command not found")

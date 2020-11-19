import os
import sys
import re



while True:
    # requirement 1 make $ as ps1
    print("$", end="")
    if 'PS1' in os.environ:
        os.write(1, os.environ['PS1'].encode())
    try:
        user_input_string = input().strip()
        user_input_array = user_input_string.split()
    except EOFError:
        sys.exit(1)
    # user_input = input()
    print("command: ", user_input_string)
    # requirement 4 part a exit
    if "exit" in user_input_array:
        sys.exit(0)
    # requirement 4 part b change directory
    if user_input_array[0] == "cd":
        print("call change directory function")

    # requirements 3 part a handles expected user error
    else:
        print("command not found")

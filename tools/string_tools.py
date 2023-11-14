

import random
import string

def get_random_printable_string(length):
    # choose from all printable
    letters = string.printable
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str

def get_random_string(length):
    # choose from all printable
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str


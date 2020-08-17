import os


def print_correct_format():
    """Prints examples of correct command format and exits code

    Helper Function that assists, when user enters invalid command
    to execute code
    """

    print("Following are the correct command examples:\n")
    print("python3 weatherman.py /path-to-zipfile -e 2011 ")
    print("python3 weatherman.py /path-to-zipfile -e 2016 -a 2007/6 -c 2009/5\n")
    exit()


def get_file_extension(file_name):
    """Returns file extensions
    """
    return os.path.splitext(file_name)[1]

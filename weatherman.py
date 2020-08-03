import os
import sys
import datetime as dt

from reports import year_report, month_report, month_chart
from file_handler import extract_files, handle_csv, handle_xlsx

# globals
# main data structure to store weather dataset
weather_dataset = {}


def handle_sys_argv(sys_argv):
    """Validates given sys arguments

    Args:
        sys_argv (list): Contains list of sys arguments

    Returns:
        dict: Dictionary with keys ["path","-e","-a","-c"],
              if found in list, and their corresponding values
    """

    argv = {}
    if len(sys_argv) > 3:
        argv["path"] = sys_argv[1]

        if "-e" in sys_argv:
            # the next element to flag is its value
            try:
                arg_e = sys_argv[sys_argv.index("-e")+1]
                date = dt.datetime.strptime(arg_e, "%Y")
                argv["-e"] = int(date.strftime("%Y"))
            except:
                print("Invalid year given for flag -e")
                print_correct_format()

        if "-a" in sys_argv:
            try:
                arg_a = sys_argv[sys_argv.index("-a")+1]
                date = dt.datetime.strptime(arg_a, "%Y/%m")
                argv["-a"] = (int(date.strftime("%Y")),
                              int(date.strftime("%m")))
            except:
                print("Invalid arguments given for flag -a")
                print_correct_format()

        if "-c" in sys_argv:
            try:
                arg_c = sys_argv[sys_argv.index("-c")+1]
                date = dt.datetime.strptime(arg_c, "%Y/%m")
                argv["-c"] = (int(date.strftime("%Y")),
                              int(date.strftime("%m")))
            except:
                print("Invalid arguments given for flag -c")
                print_correct_format()
    else:
        print("Missing arguments")
        print_correct_format()

    return argv


def print_correct_format():
    """Prints examples of correct command format and exits code

    Helper Function that assists, when user enters invalid command
    to execute code
    """

    print("Following are the correct command examples:\n")
    print("python3 weatherman.py /path-to-zipfile -e 2011 ")
    print("python3 weatherman.py /path-to-zipfile -e 2016 -a 2007/6" +
          " -c 2009/5\n")
    exit()


def date_exists(year, month=-1):
    """Returns True if given month/year exists in weather dataset

    Args:
        month (int, optional)
        year (int)

    Returns:
        [Boolean]
    """

    if year in weather_dataset:
        if month != -1:
            if month in weather_dataset[year]:
                return True
            else:
                return False
        return True
    else:
        return False


def get_month_data(files_path, file_name):
    
    if file_name.endswith(".txt"):
        year, month, month_data = handle_csv(files_path, file_name, ",")
        return (year, month, month_data)

    elif file_name.endswith(".tsv"):
        year, month, month_data = handle_csv(files_path, file_name, "\t")
        return (year, month, month_data)

    elif file_name.endswith(".xlsx"):
        year, month, month_data = handle_xlsx(files_path, file_name)
        return (year, month, month_data)
    
    # print()

if __name__ == "__main__":

    argv = handle_sys_argv(sys.argv)
    zip_path = argv["path"].strip()
    filenames = extract_files(zip_path)
    files_path = "./weatherfiles"

    for file_name in filenames:
        if file_name.endswith(".txt"):
            year, month, month_data = handle_csv(files_path, file_name, ",")

        elif file_name.endswith(".tsv"):
            year, month, month_data = handle_csv(files_path, file_name, "\t")

        elif file_name.endswith(".xlsx"):
            year, month, month_data = handle_xlsx(files_path, file_name)

        # adding month data to weather_dataset datastructure
        if year in weather_dataset:
            weather_dataset[year][month] = month_data
        else:
            weather_dataset[year] = dict()
            weather_dataset[year][month] = month_data

    # checking for arguments options
    if "-e" in argv:
        year = argv["-e"]
        if date_exists(year):
            year_report(weather_dataset, year)
        else:
            print("The -e flag is given a year that does " +
                  "not exist in data set")
    if "-a" in argv:
        year, month = argv["-a"]
        if date_exists(year, month):
            month_report(weather_dataset, year, month)
        else:
            print("The -a flag is given a year/month that does " +
                  "not exist in data set")
    if "-c" in argv:
        year, month = argv["-c"]
        if date_exists(year, month):
            month_chart(weather_dataset, year, month)
        else:
            print("The -c flag is given a year/month that does " +
                  "not exist in data set")

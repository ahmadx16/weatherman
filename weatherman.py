import os
import sys
import argparse
import datetime as dt


from reports import year_report, month_report, month_chart
from file_handler import extract_files, handle_csv, handle_xlsx

# globals
# main data structure to store weather dataset
weather_dataset = {}


def handle_sys_argv():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', type=dir_path,
        help="path to folder containing weatherfiles.zip")
    parser.add_argument(
        '-e', nargs='?', type=check_year,
        help="enter year to get yearly report")
    parser.add_argument(
        '-a', nargs='?', type=check_month_year,
        help="enter year/month to get monthly report")
    parser.add_argument(
        '-c', nargs='?', type=check_month_year,
        help="enter year/month to get monthly chart")

    args = parser.parse_args()
    return args


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"readable_dir:{path} is not a valid path")


def check_month_year(date):
    try:
        date = dt.datetime.strptime(date, "%Y/%m")
        return date
    except:
        raise argparse.ArgumentTypeError(
            f"Date: {date} is not a valid date.\n"
            "Corrent format e.g. 2012/6")


def check_year(date):
    try:
        date = dt.datetime.strptime(date, "%Y")
        return date
    except:
        raise argparse.ArgumentTypeError(
            f"Year: {date} is not a valid date.\n" +
            "Correct year e.g. 2011")


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


def report_generator(args):
    # checking for arguments options
    if args.e:
        year = int(args.e.strftime("%Y"))
        if date_exists(year):
            year_report(weather_dataset, year)
        else:
            print("The -e flag is given a year that does " +
                  "not exist in data set")
    if args.a:
        year, month = args.a.strftime("%Y %m").split()
        year, month = int(year), int(month)
        if date_exists(year, month):
            month_report(weather_dataset, year, month)
        else:
            print("The -a flag is given a year/month that does " +
                  "not exist in data set")
    if args.c:
        year, month = args.c.strftime("%Y %m").split()
        year, month = int(year), int(month)
        if date_exists(year, month):
            month_chart(weather_dataset, year, month)
        else:
            print("The -c flag is given a year/month that does " +
                  "not exist in data set")


def add_to_dataset(year, month, month_data):
    if year in weather_dataset:
        weather_dataset[year][month] = month_data
    else:
        weather_dataset[year] = dict()
        weather_dataset[year][month] = month_data


if __name__ == "__main__":

    args = handle_sys_argv()
    print(args)

    zip_path = args.path.strip()
    filenames = extract_files(zip_path)
    files_path = "./weatherfiles"

    for file_name in filenames:
        data = get_month_data(files_path, file_name)
        if data:
            year, month, month_data = data
            add_to_dataset(year, month, month_data)

    report_generator(args)

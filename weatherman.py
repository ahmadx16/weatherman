import os
import sys
import csv
import datetime as dt
import zipfile

import xlrd

from report_calculator import calculate, get_attr_values, get_max_temp,\
    get_min_temp, get_mean_temp


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


def extract_files(path):
    """Takes path to zip file, and extracts is on current dir. 

    Args:
        path (string): path to zip file 

    Returns:
        list of str: List of filenames
    """

    try:
        with zipfile.ZipFile(os.path.join(path, "weatherfiles.zip"), 'r')\
                as zip_ref:
            for file in zip_ref.namelist():
                if file.startswith('weatherfiles/'):
                    zip_ref.extract(file)
    except:
        print("Cannot find weatherfiles.zip on provided path.")
        exit()
    else:
        filenames = os.listdir("./weatherfiles")
        return filenames


def clean_data_types(day_data):
    """Converts string data relevent type

    Args:
        day_data (dict): Contains string readings of row
    """

    for k, attr in day_data.items():
        if k == "PKT" or k == "PKST":
            day_data[k] = string_to_date(attr)

        elif k == "Events":
            event = attr
            if event == '':
                day_data[k] = None

        # converts attributes values to float
        elif (k == "Mean VisibilityKm" or k == "Max VisibilityKm" or
              k == "Min VisibilitykM" or k == "Precipitationmm" or
              k == "Mean Sea Level PressurehPa"):

            if attr != '':
                day_data[k] = float(attr)
            else:
                day_data[k] = None

        # converts attributes values to int
        else:
            if attr != '':
                day_data[k] = int(attr)
            else:
                day_data[k] = None


def handle_csv(path, file_name, delim):
    """Extracts the weather readings of a month present in csv files

    Args:
        path (string): path of the directory where file exists
        file_name (string): name of file.
        delim (string): The delimeter in which file is encoded

    Returns:
       (int, int, list[dic]): year, month, month_data
    """

    cols = []
    month_data = []
    with open(os.path.join(path, file_name), 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=delim)
        cols = next(csvreader)

        for row in csvreader:
            day_data = {cols[i].strip(): attr for i, attr in enumerate(row)}
            clean_data_types(day_data)
            month_data.append(day_data)

    # getting year and month
    date = month_data[0][list(month_data[0].keys())[0]]
    year = int(date.strftime("%Y"))
    month = int(date.strftime("%m"))

    return (year, month, month_data)


def handle_xlsx(path, file_name):
    """Extracts the weather readings of a month present in .xlsx file

    Args:
        path (string): path of the directory where file exists
        file_name (string): name of file.

    Returns:
        (int, int, list[dic]): year, month, month_data
    """

    book = xlrd.open_workbook(os.path.join(path, file_name))
    sheet = book.sheet_by_index(0)

    month_data = []
    cols = sheet.row_values(0)
    # getting year and month from 2nd row
    date = string_to_date(sheet.row_values(2)[0])
    year = int(date.strftime("%Y"))
    month = int(date.strftime("%m"))

    for i in range(1, sheet.nrows):
        day_row = sheet.row_values(i)
        # converts the list of day data into dictionary
        day_data = {cols[i].strip(): attr
                    for i, attr in enumerate(day_row)
                    if attr is not None}
        clean_data_types(day_data)
        month_data.append(day_data)
    return (year, month, month_data)


def year_report(year):
    """Prints Report of a given year

    The report prints Max Temperature,Min Temperature and
    Min Humidity of a given year.

    Args:
        year (int): This year's report is printed
    """

    max_temp, max_temp_date = get_max_temp(
        weather_dataset, "Max TemperatureC", year)

    min_temp, min_temp_date = get_min_temp(
        weather_dataset, "Min TemperatureC", year)

    min_humid, min_humid_date = get_min_temp(
        weather_dataset, "Min Humidity", year)

    print("-- Year {} Report --".format(year))
    print("Highest: {0}C on {1} {2}"
          .format(max_temp,
                  max_temp_date.strftime("%B"),
                  max_temp_date.strftime("%d")
                  ))
    print("Lowest: {0}C on {1} {2}"
          .format(min_temp,
                  min_temp_date.strftime("%B"),
                  min_temp_date.strftime("%d")
                  ))
    print("Humidity: {0}% on {1} {2}\n"
          .format(min_humid,
                  min_humid_date.strftime("%B"),
                  min_humid_date.strftime("%d")
                  ))


def month_report(year, month):
    """Prints Report of a given month and year

       It prints 'Highest Average temperature', 'Lowest Average
       Temperature' and Averege Mean Humidity of a given month.
    """

    avg_max_temp, month_date = calculate(
        weather_dataset, "Max TemperatureC", "mean", year, month)

    avg_min_temp, month_date = calculate(
        weather_dataset, "Min TemperatureC", "mean", year, month)

    avg_mean_humid, month_date = calculate(
        weather_dataset, "Mean Humidity", "mean", year, month)

    month_name = month_date.strftime("%B")

    print("-- {} {} Report --".format(month_name, year))
    print("Average Highest: {:.0f}C ".format(round(avg_max_temp, 1)))
    print("Average Lowest: {:.0f}C".format(round(avg_min_temp, 1)))
    print("Average Mean Humidity: {:.0f}% \n".format(round(avg_mean_humid, 1)))


class Colors:
    """Class for colored text on console 
    """

    BLUE = '\033[94m'
    RED = '\033[91m'
    ENDC = '\033[0m'


def month_chart(year, month):
    """Prints color charts on console of a given month
    """

    high_temps = get_attr_values(
        weather_dataset, "Max TemperatureC",  year, month)

    low_temps = get_attr_values(
        weather_dataset, "Min TemperatureC", year, month)

    month_name = high_temps[0][1].strftime("%B")

    # Saving max temperature and min temperature in dictionaries
    # key is datetime object
    high_temps = {attr[1]: attr[0] for attr in high_temps}
    low_temps = {attr[1]: attr[0] for attr in low_temps}

    # prints colored chart
    print("{0} {1}".format(month_name, year))
    for k in high_temps:
        # low temp chart
        print(k.strftime("%d"), end=" ")
        for _ in range(low_temps[k]):
            print(Colors.BLUE + "+" + Colors.ENDC, end="")
        # high temp chart
        for _ in range(high_temps[k]):
            print(Colors.RED + "+" + Colors.ENDC, end="")

        print("", str(low_temps[k])+"C - ", end="")
        print(str(high_temps[k])+"C", end='\n')


def string_to_date(date_string):
    """Converts the string date, in format yyyy-mm-dd, to datetime   
    """

    try:
        date = dt.datetime.strptime(date_string, "%Y-%m-%d")
    except:
        print("Invalid format of date found in dataset")
    else:
        return date


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
            year_report(year)
        else:
            print("The -e flag is given a year that does " +
                  "not exist in data set")
    if "-a" in argv:
        year, month = argv["-a"]
        if date_exists(year, month):
            month_report(year, month)
        else:
            print("The -a flag is given a year/month that does " +
                  "not exist in data set")
    if "-c" in argv:
        year, month = argv["-c"]
        if date_exists(year, month):
            month_chart(year, month)
        else:
            print("The -c flag is given a year/month that does " +
                  "not exist in data set")

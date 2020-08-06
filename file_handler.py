import os
import shutil
import zipfile
import csv
import datetime as dt

import xlrd

from assist_functions import date_to_int


# attributes that are relevent to calculations
REQUIRED_ATTRIBUTES = (
    "PKT",
    "PKST",
    "Max TemperatureC",
    "Min TemperatureC",
    "Min Humidity",
    "Mean Humidity",
)


def filter_attributes(day_data):
    """ Discards non relevent attributes from datastructure
    """

    for key in list(day_data):
        if key not in REQUIRED_ATTRIBUTES:
            del day_data[key]


def is_date_in_filename(arg, file_name, check_month=False):
    """Check year and month in filename
    """

    if arg.strftime("%Y") in file_name:
        if check_month:
            if arg.strftime("%b") in file_name:
                return True
        else:
            return True

    return False


def is_file_relevent(args, file_name):
    """ Checks filename is relevent to user query
    """

    if file_name.startswith('weatherfiles/'):
        if args.e:
            return is_date_in_filename(args.e, file_name)
        if args.a:
            return is_date_in_filename(args.a, file_name, check_month=True)
        if args.c:
            return is_date_in_filename(args.c, file_name, check_month=True)

    return False


def extract_files(args, path):
    """Extracts only relevent to query files on current directory 

    Returns:
        list of str: List of relevent filenames
    """

    # delete folder if it already exists
    if "weatherfiles" in os.listdir():
        shutil.rmtree("weatherfiles")

    os.mkdir("weatherfiles")

    try:
        with zipfile.ZipFile(os.path.join(path, "weatherfiles.zip"), 'r')\
                as zip_ref:
            for file_name in zip_ref.namelist():
                # check and extract only relevent files
                if is_file_relevent(args, file_name):
                    zip_ref.extract(file_name)

    except FileNotFoundError:
        print("Cannot find weatherfiles.zip on provided path.")
        exit()
    except IOError:
        print("Could not read weatherfiles.zip.")
        exit()
    else:
        filenames = os.listdir("./weatherfiles")
        return filenames


def clean_data_types(day_data):
    """Converts string data relevent type

    Args:
        day_data (dict): Contains string readings of row
    """

    time_attributes = ["PKT", "PKST"]
    float_attributes = [
        "Mean VisibilityKm",
        "Max VisibilityKm",
        "Min VisibilitykM",
        "Precipitationmm",
        "Mean Sea Level PressurehPa"
    ]

    for k, attr in day_data.items():

        if k in time_attributes:
            day_data[k] = string_to_date(attr)

        elif k == "Events":
            event = attr
            if event:
                day_data[k] = None

        # converts attributes values to float
        elif k in float_attributes:
            if attr:
                day_data[k] = float(attr)
            else:
                day_data[k] = None

        # converts attributes values to int
        else:
            if attr:
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
            filter_attributes(day_data)
            clean_data_types(day_data)
            month_data.append(day_data)

    # getting year and month
    date = date_from_month_data(month_data)
    year, month = date_to_int(date)

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
    year, month = date_to_int(date)

    for i in range(1, sheet.nrows):
        day_row = sheet.row_values(i)
        # converts the list of day data into dictionary
        day_data = {cols[i].strip(): attr
                    for i, attr in enumerate(day_row)
                    if attr is not None}
        filter_attributes(day_data)
        clean_data_types(day_data)
        month_data.append(day_data)
    return (year, month, month_data)


def string_to_date(date_string):
    """Converts the string date, in format yyyy-mm-dd, to datetime   
    """

    try:
        date = dt.datetime.strptime(date_string, "%Y-%m-%d")
    except:
        print("Invalid format of date found in dataset")
    else:
        return date


def date_from_month_data(month_data):
    return month_data[0][list(month_data[0].keys())[0]]


def delete_files():
    """deletes extracted files and folder
    """

    shutil.rmtree("weatherfiles")

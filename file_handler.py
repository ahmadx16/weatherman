import os
import zipfile
import csv
import xlrd
import datetime as dt


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


def string_to_date(date_string):
    """Converts the string date, in format yyyy-mm-dd, to datetime   
    """

    try:
        date = dt.datetime.strptime(date_string, "%Y-%m-%d")
    except:
        print("Invalid format of date found in dataset")
    else:
        return date

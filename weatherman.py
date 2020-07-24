import zipfile
import os
import re
import xlrd
import sys


path = "./weatherfiles/"

# main data structure
year_dic = {}


def string_to_date(s_date):
    year, month, day = re.split("-", s_date)
    year, month, day = int(year), int(month), int(day)
    return year, month, day


def parse_file(delim, f_name):
    cols = []
    year = 0
    month = 0
    # dates is list of dictionaries of weather data
    dates = []
    file_data = open(path+f_name, 'r', errors='ignore').readlines()
    for i, line in enumerate(file_data):
        line = line.replace("\n", "")
        if i == 0:
            cols = re.split(delim, line)
        else:
            lis = re.split(delim, line)
            tmp_year, tmp_month, _ = string_to_date(lis[0])

            # error check non consistent year or month within same file
            if tmp_year != year and year != 0:
                print("error: non consistent file")
                exit()
            if tmp_month != month and month != 0:
                print("error: non consistent file")
                exit()

            year, month = tmp_year, tmp_month
            tmp_dic = {}
            for i, attr in enumerate(cols):
                tmp_dic[attr.strip()] = lis[i]
            dates.append(tmp_dic)
    return year, month, dates


def handle_xlsx(f_name):
    wb = xlrd.open_workbook(path+f_name)

    sheet = wb.sheet_by_index(0)
    for _ in range(sheet.ncols):
        pass


def printer(year_dic):
    print(len(year_dic[2012][1][0]))


def handle_sys_argv(sys_argv):
    argv_dic = {}
    if len(sys_argv) > 1:
        argv_dic["path"] = sys_argv[1]

        if "-e" in sys_argv:
            argv_dic["-e"] = sys_argv[sys_argv.index("-e")+1]
        if "-a" in sys_argv:
            argv_dic["-a"] = sys_argv[sys_argv.index("-a")+1]
        if "-c" in sys_argv:
            argv_dic["-c"] = sys_argv[sys_argv.index("-c")+1]

    return argv_dic


def year_report(year):
    year_data = year_dic[year]

    max_temp = -273
    min_temp = 1000
    min_humid = 100
    for k, month in year_data.items():
        for day in month:
            temp = day["Max TemperatureC"]
            if temp != '':
                temp = int(temp)
                if temp > max_temp:
                    max_temp = temp
            temp = day["Min TemperatureC"]
            if temp != '':
                temp = int(temp)
                if temp < min_temp:
                    min_temp = temp
            humid = day["Min Humidity"]
            if humid != '':
                humid = int(humid)
                if humid < min_humid:
                    min_humid = humid
    print(max_temp)
    print(min_temp)
    print(min_humid)


def month_report(year, month):
    pass


def month_chart(year, month):
    pass


if __name__ == "__main__":

    argv_dic = handle_sys_argv(sys.argv)

    with zipfile.ZipFile("./weatherfiles.zip", 'r') as zip_ref:
        zip_ref.extractall()
    filenames = os.listdir(path)
    for f_name in filenames:
        if f_name.endswith(".txt"):
            year, month, dates = parse_file(",", f_name)
            if year in year_dic:
                year_dic[year][month] = dates
            else:
                year_dic[year] = dict()
                year_dic[year][month] = dates

        elif f_name.endswith(".tsv"):
            year, month, dates = parse_file("\t", f_name)
        elif f_name.endswith(".xlsx"):
            handle_xlsx(f_name)
            # break

    if "-e" in argv_dic:
        year = int(argv_dic["-e"])
        year_report(year)
    if "-a" in argv_dic:
        y_m = argv_dic["-a"]
        year, month = re.split("/", y_m)
        month_report(int(year), int(month))
    if "-c" in argv_dic:
        y_m = argv_dic["-c"]
        year, month = re.split("/", y_m)
        month_chart(int(year), int(month))

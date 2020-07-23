import zipfile
import os
import re
import xlrd


path = "./weatherfiles/"


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
    for k, v in year_dic.items():
        print(k)


year_dic = {}
if __name__ == "__main__":
    with zipfile.ZipFile("./weatherfiles.zip", 'r') as zip_ref:
        zip_ref.extractall()
    filenames = os.listdir(path)
    for f_name in filenames:
        if f_name.endswith(".txt"):
            year, month, dates = parse_file(",", f_name)
            if year in year_dic:
                year_dic[year][month] = dates
            else:
                # print(year,month)
                year_dic[year] = dict()
                year_dic[year][month] = dates

        elif f_name.endswith(".tsv"):
            year, month, dates = parse_file("\t", f_name)
        elif f_name.endswith(".xlsx"):
            handle_xlsx(f_name)
            # break

    printer(year_dic)

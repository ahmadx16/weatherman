import zipfile
import os
import re
import xlrd
import sys
import datetime as dt


path = "./weatherfiles/"

# main data structure
year_dic = {}


def string_to_date(s_date):
    year, month, day = re.split("-", s_date)
    year, month, day = int(year), int(month), int(day)
    return year, month, day

# assignining relevent data types to the fields
def clean_data_types(day_dic):
    for k in day_dic:
        if k == "PKT":
            year, month, day = string_to_date(day_dic[k])
            date = dt.datetime(year, month, day)
            day_dic[k] = date

        elif k == "PKST":
            year, month, day = string_to_date(day_dic[k])
            date = dt.datetime(year, month, day)
            # this is to ensure consistency in our datastructure
            day_dic[k] = date

        elif k == "Events":
            # events are already strings
            event = day_dic[k]
            if event == '':
                day_dic[k] = None
            pass
        # floats
        elif (k == "Mean VisibilityKm" or k == "Max VisibilityKm" or
                k == "Min VisibilitykM" or k == "Precipitationmm" or
                k == "Mean Sea Level PressurehPa"):

            val = day_dic[k]
            if val != '':
                day_dic[k] = float(val)
            else:
                day_dic[k] = None

        else:
            val = day_dic[k]
            if val != '':
                day_dic[k] = int(val)
            else:
                day_dic[k] = None
    return day_dic


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
            tmp_dic = clean_data_types(tmp_dic)
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


#  --- Report Functions ---

def year_report(year):
    year_data = year_dic[year]

    max_temp = {"temp": -273, "date": None}
    min_temp = {"temp": 1000, "date": None}
    min_humid = {"humid": 100, "date": None}

    for k, month in year_data.items():
        for day in month:
            date = None
            if "PKT" in day:
                date = day["PKT"]
            elif "PKST" in day:
                date = day["PKST"]

            temp = day["Max TemperatureC"]
            if temp is not None:
                if temp > max_temp["temp"]:
                    max_temp["temp"] = temp
                    max_temp["date"] = date

            temp = day["Min TemperatureC"]
            if temp is not None:
                if temp < min_temp["temp"]:
                    min_temp["temp"] = temp
                    min_temp["date"] = date

            humid = day["Min Humidity"]
            if humid is not None:
                if humid < min_humid["humid"]:
                    min_humid["humid"] = humid
                    min_humid["date"] = date
   

    print("-- {} Yearly Report--".format(year))

    print("Highest: {0}C on {1} {2}"
          .format(max_temp["temp"],
                  max_temp["date"].strftime("%B"),
                  max_temp["date"].strftime("%d")
                  ))

    print("Lowest: {0}C on {1} {2}"
          .format(min_temp["temp"],
                  min_temp["date"].strftime("%B"),
                  min_temp["date"].strftime("%d")
                  ))
    print("Humidity: {0}% on {1} {2}"
          .format(min_humid["humid"],
                  min_humid["date"].strftime("%B"),
                  min_humid["date"].strftime("%d")
                  ))


def month_report(year, month):
    month_data = year_dic[year][month]
    
    max_temp = {"temp": -273, "date": None}
    min_temp = {"temp": 1000, "date": None}
    mean_humid = {"humid": 0, "date": None}
    
    for day in month_data:
        date = None
        if "PKT" in day:
            date = day["PKT"]
        elif "PKST" in day:
            date = day["PKST"]

        temp = day["Mean TemperatureC"]
        if temp is not None:
            if temp > max_temp["temp"]:
                max_temp["temp"] = temp
                max_temp["date"] = date

        if temp is not None:
            if temp < min_temp["temp"]:
                min_temp["temp"] = temp
                min_temp["date"] = date

        humid = day["Min Humidity"]
        if humid is not None:
            mean_humid["humid"] += humid
            mean_humid["date"] = date

        mean_humid["humid"] = mean_humid["humid"]/len(month_data)

    print("--  Month {} Report--".format(month))

    print("Highest Average: {0}C "
          .format(max_temp["temp"] ))

    print("Lowest Average: {0}C"
          .format(min_temp["temp"]))
    print("Average Mean Humidity: {0}% "
          .format(mean_humid["humid"]))


class bcolors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    

def month_chart(year, month):
    month_data = year_dic[year][month]
    
    high_temps ={}
    low_temps={}

    g_date=None
    for day in month_data:
        date = None
        if "PKT" in day:
            date = day["PKT"]
        elif "PKST" in day:
            date = day["PKST"]
        g_date=date
        temp = day["Max TemperatureC"]
        if temp is not None:
            high_temps[date.strftime("%d")] = temp

        temp = day["Min TemperatureC"]
        if temp is not None:
            low_temps[date.strftime("%d")] = temp


    print("{0} {1}".format(g_date.strftime("%B"),year)) 

    for k in high_temps:
        # low temp chart
        print(k,end=" ")
        for _ in range(low_temps[k]):
            print(bcolors.BLUE + "+" + bcolors.ENDC, end="")
        
        # high temp chart
        for _ in range(high_temps[k]):
            print(bcolors.RED + "+" + bcolors.ENDC, end="")

        print("",str(low_temps[k])+"C - ",end="")
        print(str(high_temps[k])+"C")
        
 
    


# MAIN
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




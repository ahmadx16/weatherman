import os
import sys
import shutil
import argparse
import datetime as dt


from report_printer import ReportPrinter
from file_handler import FileHandler


class WeatherMan:

    def __init__(self):
        # Initializing instance attributes
        self.args = 0
        self.weather_dataset = {}
        self.file_handler = FileHandler()
        self.report_printer = ReportPrinter()

    def handle_sys_argv(self):
        """Validates and parses sys arguments
        """

        parser = argparse.ArgumentParser()
        parser.add_argument(
            'path', type=self.check_dir_path,
            help="path to folder containing weatherfiles.zip")
        parser.add_argument(
            '-e', nargs='?', type=self.check_year,
            help="enter year to get yearly report")
        parser.add_argument(
            '-a', nargs='?', type=self.check_month_year,
            help="enter year/month to get monthly report")
        parser.add_argument(
            '-c', nargs='?', type=self.check_month_year,
            help="enter year/month to get monthly chart")
        args = parser.parse_args()

        if args.e == args.a == args.c == None:
            print("No arguments given")
            self.print_correct_format()
            exit()

        self.args = args

    def create_dataset(self):
        """Creates weatherman_dataset based on given arguments
        """
        zip_path = self.args.path.strip()
        filenames = self.file_handler.extract_files(self.args, zip_path)
        files_path = "./weatherfiles"

        for file_name in filenames:
            year, month, month_data = weatherman_obj.get_month_data(files_path, file_name)
            if month_data:
                self.add_to_dataset(self.weather_dataset, year, month, month_data)

    def print_report(self):
        """Uses ReportPrinter class to print report
        """
        self.report_printer.generate_reports(self.weather_dataset, self.args)

    def check_dir_path(self, path):
        """ path check for argparse
        """

        if os.path.isdir(path):
            return path

        raise argparse.ArgumentTypeError(
            f"readable_dir:{path} is not a valid path")

    def check_month_year(self, date):
        """ date check for argparse
        """

        try:
            return dt.datetime.strptime(date, "%Y/%m")
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Date: {date} is not a valid date.\n"
                "Correct format e.g. 2012/6")

    def check_year(self, date):
        """ year check for argparse
        """

        try:
            return dt.datetime.strptime(date, "%Y")
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Year: {date} is not a valid date.\n" +
                "Correct year e.g. 2011")

    def print_correct_format(self):
        """Prints examples of correct command format and exits code

        Helper Function that assists, when user enters invalid command
        to execute code
        """

        print("Following are the correct command examples:\n")
        print("python3 weatherman.py /path-to-zipfile -e 2011 ")
        print("python3 weatherman.py /path-to-zipfile -e 2016 -a 2007/6 -c 2009/5\n")
        exit()

    def date_exists(self, weather_dataset, year, month=-1):
        """Returns True if given month/year exists in weather dataset
        """

        if year not in weather_dataset:
            return False
        if month != -1:
            return month in weather_dataset[year]

        return True

    def get_month_data(self, files_path, file_name):
        """ Return month data of a given file name
        """
        year = month = month_data = 0

        if file_name.endswith(".txt"):
            year, month, month_data = self.file_handler.handle_csv(files_path, file_name, ",")

        elif file_name.endswith(".tsv"):
            year, month, month_data = self.file_handler.handle_csv(files_path, file_name, "\t")

        elif file_name.endswith(".xlsx"):
            year, month, month_data = self.file_handler.handle_xlsx(files_path, file_name)

        return (year, month, month_data)

    def add_to_dataset(self, weather_dataset, year, month, month_data):
        """ adds month data to main dataset
        """

        if year in weather_dataset:
            weather_dataset[year][month] = month_data
        else:
            weather_dataset[year] = dict()
            weather_dataset[year][month] = month_data

    def delete_weatherfiles(self):
        self.file_handler.delete_files("weatherfiles")


if __name__ == "__main__":

    weatherman_obj = WeatherMan()

    weatherman_obj.handle_sys_argv()
    weatherman_obj.create_dataset()
    weatherman_obj.print_report()

    weatherman_obj.delete_weatherfiles()

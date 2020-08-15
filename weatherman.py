import os
import sys
import argparse
import datetime as dt

from report_printer import ReportPrinter
from file_handler import FileHandler
from handle_csv import HandleCsv
from handle_xlsx import HandleXlsx
from utils import print_correct_format


class WeatherMan:

    def __init__(self):
        """Initializing instance attributes
        """
        self.args = 0
        self.weather_dataset = {}
        self.file_handler = FileHandler()

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
            print_correct_format()
            exit()

        self.args = args

    def create_dataset(self):
        """Creates weatherman_dataset based on given arguments
        """
        if self.args:
            zip_path = self.args.path.strip()
            filenames = self.file_handler.extract_files(self.args, zip_path)
            files_path = "./weatherfiles"

            for file_name in filenames:
                year, month, month_data = weatherman_obj.get_month_data(files_path, file_name)
                if month_data:
                    self.add_to_dataset(self.weather_dataset, year, month, month_data)
        else:
            print('There are no args available. Please Call "handle_sys_argv" method first to handle sys arguments\n')
            exit()

    def print_report(self):
        """Uses ReportPrinter class to print report
        """
        if len(self.weather_dataset):
            report_printer = ReportPrinter(self.weather_dataset, self.args)
            report_printer.generate_reports()
        else:
            print('There is no dataset available. Call "create_dataset" method first to create dataset\n')
            exit()

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

    def handle_files(self, files_path, file_name):
        """Handle different files based on their file types
        """
        year = month = month_data = 0

        if file_name.endswith(".txt"):
            handle_csv = HandleCsv(",")
            year, month, month_data = handle_csv.handle(files_path, file_name)

        elif file_name.endswith(".tsv"):
            handle_csv = HandleCsv("\t")
            year, month, month_data = handle_csv.handle(files_path, file_name)

        elif file_name.endswith(".xlsx"):
            handle_xlsx= HandleXlsx()
            year, month, month_data = handle_xlsx.handle(files_path, file_name)
        
        return (year,month,month_data)

    def get_month_data(self, files_path, file_name):
        """ Return month data of a given file name
        """

        return self.handle_files(files_path, file_name)

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

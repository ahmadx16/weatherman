import os
import sys
import datetime as dt

from report_printer import ReportPrinter
from file_handler import FileHandler
from handle_csv import HandleCsv
from handle_xlsx import HandleXlsx
from handle_sys_arg import HandleSysArg
from utils import get_file_extension


class WeatherMan:

    extension_to_file_handler = {
        ".txt": HandleCsv,
        ".tsv": HandleCsv,
        ".xlsx": HandleXlsx
    }

    def __init__(self):
        """Initializing instance attributes"""

        self.args = 0
        self.weather_dataset = {}
        self.file_handler = FileHandler()

    def handle_sys_argv(self):
        arg_handler = HandleSysArg()
        self.args = arg_handler.handle_sys_argv()

    def create_dataset(self):
        """Creates weatherman_dataset based on given arguments"""

        if self.args:
            zip_path = self.args.path.strip()
            filenames = self.file_handler.extract_files(self.args, zip_path)
            files_path = "./weatherfiles"

            for file_name in filenames:
                year, month, month_data = weatherman_obj.get_month_data(files_path, file_name)
                if month_data:
                    self.add_to_dataset(self.weather_dataset, year, month, month_data)
        else:
            print('There are no args available.\n')
            exit()

    def print_report(self):
        """Uses ReportPrinter class to print report"""

        report_printer = ReportPrinter(self.weather_dataset, self.args)
        report_printer.generate_reports()

    def get_file_handler(self, file_name):
        """Returns relevent class based on file extension"""

        return self.extension_to_file_handler[get_file_extension(file_name)]

    def get_month_data(self, files_path, file_name):
        """Return month data of a given file name"""

        year = month = month_data = 0
        file_handler = self.get_file_handler(file_name)()
        year, month, month_data = file_handler.handle(files_path, file_name)

        return (year, month, month_data)

    def add_to_dataset(self, weather_dataset, year, month, month_data):
        """adds month data to main dataset"""

        if year in weather_dataset:
            weather_dataset[year][month] = month_data
        else:
            weather_dataset[year] = dict()
            weather_dataset[year][month] = month_data

    def delete_weatherfiles(self):
        """Deletes the extracted folder"""

        self.file_handler.delete_files("weatherfiles")


if __name__ == "__main__":

    weatherman_obj = WeatherMan()

    weatherman_obj.handle_sys_argv()
    weatherman_obj.create_dataset()
    weatherman_obj.print_report()

    weatherman_obj.delete_weatherfiles()

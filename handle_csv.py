import os
import csv
from file_handler import FileHandler

from utils import get_file_extension


class HandleCsv(FileHandler):
    """For Handeling CSV files"""

    extension_to_delimeter = {
        ".txt": ",",
        ".tsv": "\t"
    }

    def __init__(self):
        super().__init__()

    def get_delimeter(self, file_name):
        """ Return delimenter corresponding to file type"""
        return self.extension_to_delimeter[get_file_extension(file_name)]

    def handle(self, path, file_name):
        """Extracts the weather readings of a month present in csv files

        Args:
            path (string): path of the directory where file exists
            file_name (string): name of file.

        Returns:
        (int, int, list[dic]): year, month, month_data
        """

        delim = self.get_delimeter(file_name)

        cols = []
        month_data = []
        try:
            with open(os.path.join(path, file_name), 'r') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=delim)
                cols = next(csvreader)

                for row in csvreader:
                    day_data = {cols[i].strip(): attr for i, attr in enumerate(row)}
                    self.filter_attributes(day_data)
                    self.clean_data_types(day_data)
                    if day_data:
                        month_data.append(day_data)

            # getting year and month
            date = self.date_from_month_data(month_data)
            return (date.year, date.month, month_data)

        except (AttributeError, ValueError):
            print(f"File {file_name} contains invalid format\n")
            exit()
        except IOError:
            print(f"Could not read file {file_name}\n")
            exit()
        except IndexError:
            print(f"File {file_name} does not contain enough data\n")
            exit()

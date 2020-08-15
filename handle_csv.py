import os
import csv
from file_handler import FileHandler

class HandleCsv(FileHandler):
    """For Handeling CSV files
    """

    def __init__(self,delim):
        super().__init__()
        self.delim = delim

    def handle(self, path, file_name):
        """Extracts the weather readings of a month present in csv files

        Args:
            path (string): path of the directory where file exists
            file_name (string): name of file.

        Returns:
        (int, int, list[dic]): year, month, month_data
        """

        cols = []
        month_data = []
        with open(os.path.join(path, file_name), 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=self.delim)
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
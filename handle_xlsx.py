import os
import xlrd

from file_handler import FileHandler


class HandleXlsx(FileHandler):
    """For Handeling Xlsx files"""

    def __init__(self):
        super().__init__()

    def handle(self, path, file_name):
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
        date = self.string_to_date(sheet.row_values(2)[0])

        for i in range(1, sheet.nrows):
            day_row = sheet.row_values(i)
            # converts the list of day data into dictionary
            day_data = {cols[i].strip(): attr
                        for i, attr in enumerate(day_row)
                        if attr is not None}
            self.filter_attributes(day_data)
            self.clean_data_types(day_data)
            month_data.append(day_data)
        return (date.year, date.month, month_data)

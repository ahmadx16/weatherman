import os
import shutil
import zipfile
import datetime as dt


class FileHandler:
    """Class to handle file related functions"""

    # class attributes that are relevent to calculations
    REQUIRED_ATTRIBUTES = (
        "PKT",
        "PKST",
        "Max TemperatureC",
        "Min TemperatureC",
        "Min Humidity",
        "Mean Humidity",
    )

    def filter_attributes(self, day_data):
        """ Discards non relevent attributes from datastructure"""

        for key in list(day_data):
            if key not in self.REQUIRED_ATTRIBUTES:
                del day_data[key]

    def is_date_in_filename(self, arg, file_name, check_month=False):
        """Check year and month in filename"""

        if arg.strftime("%Y") not in file_name:
            return False

        if check_month:
            return arg.strftime("%b") in file_name

        return True

    def is_file_relevent(self, args, file_name):
        """ Checks filename is relevent to user query"""

        if file_name.startswith('weatherfiles/'):
            if args.e:
                if self.is_date_in_filename(args.e, file_name):
                    return True
            if args.a:
                if self.is_date_in_filename(args.a, file_name, check_month=True):
                    return True
            if args.c:
                if self.is_date_in_filename(args.c, file_name, check_month=True):
                    return True

        return False

    def extract_files(self, args, path):
        """Extracts only relevent to query files on current directory 

        Returns:
            list of str: List of relevent filenames
        """

        # delete folder if it already exists
        if "weatherfiles" in os.listdir():
            shutil.rmtree("weatherfiles")

        os.mkdir("weatherfiles")

        try:
            with zipfile.ZipFile(os.path.join(path, "weatherfiles.zip"), 'r') as zip_ref:
                for file_name in zip_ref.namelist():
                    # check and extract only relevent files
                    if self.is_file_relevent(args, file_name):
                        zip_ref.extract(file_name)

        except FileNotFoundError:
            print("Cannot find weatherfiles.zip on provided path.")
            exit()
        except IOError:
            print("Could not read weatherfiles.zip.")
            exit()
        else:
            filenames = os.listdir("./weatherfiles")
            return filenames

    def clean_data_types(self, day_data):
        """Converts string data relevent type

        Args:
            day_data (dict): Contains string readings of row
        """

        time_attributes = ["PKT", "PKST"]
        float_attributes = [
            "Mean VisibilityKm",
            "Max VisibilityKm",
            "Min VisibilitykM",
            "Precipitationmm",
            "Mean Sea Level PressurehPa"
        ]

        for k, attr in day_data.items():
            if k in time_attributes:
                day_data[k] = self.string_to_date(attr)

            elif k == "Events":
                day_data[k] = attr if attr else None

            # converts attributes values to float
            elif k in float_attributes:
                day_data[k] = float(attr) if attr else None

            # converts attributes values to int
            else:
                day_data[k] = int(attr) if attr else None

    def string_to_date(self, date_string):
        """Converts the string date, in format yyyy-mm-dd, to datetime"""

        try:
            date = dt.datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            print("Invalid format of date found in dataset")
        else:
            return date

    def date_from_month_data(self, month_data):
        """Returns first date from month"""

        return month_data[0][list(month_data[0].keys())[0]]

    def delete_files(self, folder_name):
        """deletes extracted files and folder"""

        shutil.rmtree(folder_name)

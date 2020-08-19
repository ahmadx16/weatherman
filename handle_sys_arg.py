import os
import argparse
import datetime as dt

from utils import print_correct_format


class HandleSysArg:
    """Handles sys arguments"""

    def handle_sys_argv(self):
        """Validates and parses sys arguments"""

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
            print("No arguments given. You must at least use one out of -e -a -c in arguments")
            print_correct_format()

        return args

    def check_dir_path(self, path):
        """path check for argparse"""

        if os.path.isdir(path):
            return path

        raise argparse.ArgumentTypeError(
            f"readable_dir:{path} is not a valid path")

    def check_month_year(self, date):
        """date check for argparse"""

        try:
            return dt.datetime.strptime(date, "%Y/%m")
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Date: {date} is not a valid date.\n"
                "Correct format e.g. 2012/6")

    def check_year(self, date):
        """year check for argparse"""

        try:
            return dt.datetime.strptime(date, "%Y")
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Year: {date} is not a valid date.\n" +
                "Correct year e.g. 2011")

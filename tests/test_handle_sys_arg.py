import pytest
import datetime as dt
from argparse import ArgumentTypeError

from handle_sys_arg import HandleSysArg

arg_handler = HandleSysArg()


def test_check_dir_path():
    path = "./tests/MockData/"
    actual_path = arg_handler.check_dir_path(path)
    assert path == actual_path

    # invalid path check
    with pytest.raises(ArgumentTypeError):
        arg_handler.check_dir_path("./INVALID_PATH")


def test_check_month_year():
    year_month = "2011/4"
    expected_date_year_month = dt.datetime.strptime(year_month, "%Y/%m")
    actual_date_year_month = arg_handler.check_month_year(year_month)
    assert actual_date_year_month == actual_date_year_month

    # invalid date format check
    with pytest.raises(ArgumentTypeError):
        arg_handler.check_month_year("2019-12-12")


def test_check_year():
    year = "2019"
    expected_date_year = dt.datetime.strptime(year, "%Y")
    actual_date_year = arg_handler.check_year(year)
    assert actual_date_year == actual_date_year

    # invalid date format check
    with pytest.raises(ArgumentTypeError):
        arg_handler.check_year("ninety nine")
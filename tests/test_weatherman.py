import pytest
import datetime as dt
from argparse import ArgumentTypeError

from weatherman import WeatherMan
from test_data import expected_file_month_data
from test_data import weather_dataset

weatherman = WeatherMan()

def test_check_dir_path():
    path = "./tests/MockData/"
    actual_path = weatherman.check_dir_path(path)
    assert path == actual_path

    # invalid path check
    with pytest.raises(ArgumentTypeError):
        weatherman.check_dir_path("./INVALID_PATH")


def test_check_month_year():
    year_month = "2011/4"
    expected_date_year_month = dt.datetime.strptime(year_month, "%Y/%m")
    actual_date_year_month = weatherman.check_month_year(year_month)
    assert actual_date_year_month == actual_date_year_month

    # invalid date format check
    with pytest.raises(ArgumentTypeError):
        weatherman.check_month_year("2019-12-12")


def test_check_year():
    year = "2019"
    expected_date_year = dt.datetime.strptime(year, "%Y")
    actual_date_year = weatherman.check_year(year)
    assert actual_date_year == actual_date_year

    # invalid date format check
    with pytest.raises(ArgumentTypeError):
        weatherman.check_year("ninety nine")


@pytest.mark.parametrize("year,month,expected", [
    (2008, -1, False),
    (2012, -1, True),
    (2012, 1, False),
    (2012, 3, True),
    (2014, 7, True)
])
def test_date_exists(year, month, expected):
    """Tests 'date_exists'
    """
    assert expected == weatherman.date_exists(weather_dataset, year, month)


def test_get_month_data():
    """ Testing csv, tsv, and xlsx files from 'get_month_data'
    """

    actual_txt_data = weatherman.get_month_data("./tests/MockData/", "test_file.txt")
    actual_tsv_data = weatherman.get_month_data("./tests/MockData/", "test_file.tsv")
    actual_xlsx_data = weatherman.get_month_data("./tests/MockData/", "test_file.xlsx")

    assert actual_txt_data == (2004, 7, expected_file_month_data)
    assert actual_tsv_data == (2004, 7, expected_file_month_data)
    assert actual_xlsx_data == (2004, 7, expected_file_month_data)


def test_add_to_dataset():
    test_dataset = {}
    weatherman.add_to_dataset(test_dataset, 2010, 1, [1, 2, 3])
    assert {2010: {1: [1, 2, 3]}} == test_dataset
    weatherman.add_to_dataset(test_dataset, 2010, 2, [2, 4, 6])
    assert {2010: {1: [1, 2, 3], 2: [2, 4, 6]}} == test_dataset

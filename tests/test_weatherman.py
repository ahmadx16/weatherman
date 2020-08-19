import pytest
import datetime as dt
from argparse import ArgumentTypeError

from weatherman import WeatherMan
from test_data import expected_file_month_data
from test_data import weather_dataset

weatherman = WeatherMan()


def test_get_month_data():
    """ Testing csv, tsv, and xlsx files from 'get_month_data' """

    actual_txt_data = weatherman.get_month_data("./tests/MockData/", "test_file.txt")
    actual_tsv_data = weatherman.get_month_data("./tests/MockData/", "test_file.tsv")
    actual_xlsx_data = weatherman.get_month_data("./tests/MockData/", "test_file.xlsx")

    actual_values = (actual_txt_data,
                     actual_tsv_data,
                     actual_xlsx_data
                     )
    expected_values = ((2004, 7, expected_file_month_data),
                       (2004, 7, expected_file_month_data),
                       (2004, 7, expected_file_month_data)
                       )
    assert actual_values == expected_values


def test_add_to_dataset():
    test_dataset = {}
    weatherman.add_to_dataset(test_dataset, 2010, 1, [1, 2, 3])
    assert {2010: {1: [1, 2, 3]}} == test_dataset
    weatherman.add_to_dataset(test_dataset, 2010, 2, [2, 4, 6])
    assert {2010: {1: [1, 2, 3], 2: [2, 4, 6]}} == test_dataset

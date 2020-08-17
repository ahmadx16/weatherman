import pytest
import datetime as dt

from file_handler import FileHandler
from test_data import weather_dataset
from test_data import test_attributes_day_data, expected_valid_day_data
from test_data import string_day_data, expected_valid_type_day_data
from test_data import expected_file_month_data
from test_data import arg_test_obj, extracted_file_names_expected
from test_data import string_day_data_none, expected_valid_day_data_none

file_handler = FileHandler()


def test_filter_attributes():
    """Test 'filter_attributes'"""

    file_handler.filter_attributes(test_attributes_day_data)
    assert expected_valid_day_data == test_attributes_day_data


@pytest.mark.parametrize("date,file_name,check_month,expected", [
    (dt.datetime(2012, 3, 3), "somefile2012", False, True),
    (dt.datetime(2012, 3, 3), "somefile2012", True, False),
    (dt.datetime(2012, 3, 3), "somefile2012Mar", True, True),
    (dt.datetime(2012, 3, 3), "somefileMar", True, False),
])
def test_is_date_in_filename(date, file_name, check_month, expected):
    """test 'is_date_in_filename' """
    assert file_handler.is_date_in_filename(date, file_name, check_month=check_month) == expected


@pytest.mark.parametrize("file_name, expected", [
    ("weatherfiles/somefile2012", True),
    ("weatherfiles/somefile2013May", True),
    ("weatherfiles/somefile2014Jun", True),
    ("weatherfiles/somefile2011Jun", False),

])
def test_is_file_relevent(file_name, expected):
    """Test 'is_file_relevent'"""
    assert expected == file_handler.is_file_relevent(arg_test_obj, file_name)


def test_extract_files():
    """Test 'extract_files'"""
    extracted_file_names_actual = file_handler.extract_files(arg_test_obj, "./tests/MockData/")
    assert extracted_file_names_actual.sort() == extracted_file_names_expected.sort()


@pytest.mark.parametrize("string_date,date", [
    ("2000-3-3", dt.datetime(2000, 3, 3)),
    ("2012-4-13", dt.datetime(2012, 4, 13)),
    ("2015-6-23", dt.datetime(2015, 6, 23)),
    ("2050-7-30", dt.datetime(2050, 7, 30)),
])
def test_string_to_date(string_date, date, capsys):
    """Test 'string_to_date'"""
    assert file_handler.string_to_date(string_date) == date

    # Testing exception case
    file_handler.string_to_date("123a4321")
    exception_output = capsys.readouterr()
    assert exception_output.out == "Invalid format of date found in dataset\n"


def test_clean_data_types():
    """Test 'clean data types'"""

    file_handler.clean_data_types(string_day_data)
    file_handler.clean_data_types(string_day_data_none)
    assert string_day_data == expected_valid_type_day_data
    assert string_day_data_none == expected_valid_day_data_none

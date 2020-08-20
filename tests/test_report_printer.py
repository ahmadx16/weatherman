import pytest

from test_data import weather_dataset, arg_test_obj
from report_printer import ReportPrinter

report_printer = ReportPrinter(weather_dataset, arg_test_obj)


@pytest.mark.parametrize("year,month,expected", [
    (2008, -1, False),
    (2012, -1, True),
    (2012, 1, False),
    (2012, 3, True),
    (2014, 7, True)
])
def test_date_exists(year, month, expected):
    """Tests 'date_exists'"""
    assert expected == report_printer.date_exists(year, month)

import pytest
import datetime as dt
import statistics
import report_calculator

from test_data import weather_dataset
from test_data import expected_max_col_2012_3, expected_min_col_2012_3, expected_min_col_2012_4
from test_data import expected_max_col_2012, expected_min_col_2012
from test_data import expected_max_2012, expected_max_2014, expected_min_2014, expected_min_2014_7
from test_data import expected_max_mean_2014, expected_max_mean_2012, expected_min_mean_2014, expected_min_mean_2014_7


def test_get_month_attr_values():
    """Tests "get_month_attr"  
    """

    month_data = weather_dataset[2012][3]

    actual_max_2012_3 = report_calculator.get_month_attr_values(month_data, "Max TemperatureC")
    actual_min_2012_3 = report_calculator.get_month_attr_values(month_data, "Min TemperatureC")

    assert actual_max_2012_3 == expected_max_col_2012_3
    assert actual_min_2012_3 == expected_min_col_2012_3


def test_get_attr_values():
    """ Tests "get_attr_values" 
    """

    # Getting Actual values of get_attr_values
    actual_min_2012_3 = report_calculator.get_attr_values(weather_dataset, "Min TemperatureC", year=2012, month=3)
    actual_min_2012_4 = report_calculator.get_attr_values(weather_dataset, "Min TemperatureC", year=2012, month=4)
    actual_min_2012 = report_calculator.get_attr_values(weather_dataset, "Min TemperatureC", year=2012)
    actual_max_2012 = report_calculator.get_attr_values(weather_dataset, "Max TemperatureC", year=2012)

    assert expected_min_col_2012_3 == actual_min_2012_3
    assert expected_min_col_2012_4 == actual_min_2012_4
    assert expected_min_col_2012 == actual_min_2012
    assert expected_max_col_2012 == actual_max_2012


def test_get_value():
    """Test 'get_value'
    """

    # Actual Values
    actual_max_2012 = report_calculator.get_value(weather_dataset, "Max TemperatureC", "max", year=2012)
    actual_max_2014 = report_calculator.get_value(weather_dataset, "Max TemperatureC", "max", year=2014)
    actual_min_2014 = report_calculator.get_value(weather_dataset, "Min TemperatureC", "min", year=2014)
    actual_min_2014_7 = report_calculator.get_value(weather_dataset, "Min TemperatureC", "min", year=2014, month=7)

    assert expected_max_2012 == actual_max_2012
    assert expected_max_2014 == actual_max_2014
    assert expected_min_2014 == actual_min_2014
    assert expected_min_2014_7 == actual_min_2014_7


def test_get_mean_attr():
    """Test 'get_mean_attr'
    """

    # Actual Values
    actual_max_mean_2012 = report_calculator.get_mean_attr(weather_dataset, "Max TemperatureC", year=2012)
    actual_max_mean_2014 = report_calculator.get_mean_attr(weather_dataset, "Max TemperatureC", year=2014)
    actual_min_mean_2014_ = report_calculator.get_mean_attr(weather_dataset, "Min TemperatureC", year=2014)
    actual_min_mean_2014_7 = report_calculator.get_mean_attr(weather_dataset, "Min TemperatureC", year=2014, month=7)

    assert expected_max_mean_2012 == actual_max_mean_2012
    assert expected_max_mean_2014 == actual_max_mean_2014
    assert expected_min_mean_2014 == actual_min_mean_2014_
    assert expected_min_mean_2014_7 == actual_min_mean_2014_7

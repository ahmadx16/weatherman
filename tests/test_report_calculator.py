import pytest
import datetime as dt
import statistics
import report_calculator


# Test Data
weather_dataset = {2012: {3: [{"PKT": dt.datetime(2012, 3, 2), "Max TemperatureC": 12, "Min TemperatureC": 20},
                              {"PKT": dt.datetime(2012, 3, 3), "Max TemperatureC": 30, "Min TemperatureC": 5},
                              {"PKT": dt.datetime(2012, 3, 4), "Max TemperatureC": 57, "Min TemperatureC": 11},
                              {"PKT": dt.datetime(2012, 3, 5), "Max TemperatureC": 40, "Min TemperatureC": 18}],

                          4: [{"PKT": dt.datetime(2012, 4, 2), "Max TemperatureC": 20, "Min TemperatureC": 19},
                              {"PKT": dt.datetime(2012, 4, 5), "Max TemperatureC": 22, "Min TemperatureC": 16},
                              {"PKT": dt.datetime(2012, 4, 7), "Max TemperatureC": 25, "Min TemperatureC": 13},
                              {"PKT": dt.datetime(2012, 4, 10), "Max TemperatureC": 16, "Min TemperatureC": 5}]
                          },
                   2014: {6: [{"PKT": dt.datetime(2014, 6, 2), "Max TemperatureC": 102, "Min TemperatureC": 20},
                              {"PKT": dt.datetime(2014, 6, 3), "Max TemperatureC": 100, "Min TemperatureC": 25},
                              {"PKT": dt.datetime(2014, 6, 4), "Max TemperatureC": 510, "Min TemperatureC": 101},
                              {"PKT": dt.datetime(2014, 6, 5), "Max TemperatureC": 410, "Min TemperatureC": 110}],

                          7: [{"PKT": dt.datetime(2014, 7, 2), "Max TemperatureC": 210, "Min TemperatureC": 110},
                              {"PKT": dt.datetime(2014, 7, 5), "Max TemperatureC": 210, "Min TemperatureC": 111},
                              {"PKT": dt.datetime(2014, 7, 7), "Max TemperatureC": 105, "Min TemperatureC": 122},
                              {"PKT": dt.datetime(2014, 7, 10), "Max TemperatureC": 106, "Min TemperatureC": 120}]
                          }
                   }


def test_get_month_attr_values():
    """Tests "get_month_attr"  
    """
    month_data = [{"PKT": dt.datetime(2012, 1, 2), "Max TemperatureC": 12, "Min TemperatureC": 20},
                  {"PKT": dt.datetime(2012, 1, 3), "Max TemperatureC": 30, "Min TemperatureC": 5},
                  {"PKT": dt.datetime(2012, 1, 4), "Max TemperatureC": 57, "Min TemperatureC": 11},
                  {"PKT": dt.datetime(2012, 1, 5), "Max TemperatureC": 40, "Min TemperatureC": 18}]

    # expected max ouput
    expected_max_attr_data = [(12, dt.datetime(2012, 1, 2)),
                              (30, dt.datetime(2012, 1, 3)),
                              (57, dt.datetime(2012, 1, 4)),
                              (40, dt.datetime(2012, 1, 5))]
    # expected min ouput
    expected_min_attr_data = [(20, dt.datetime(2012, 1, 2)),
                              (5, dt.datetime(2012, 1, 3)),
                              (11, dt.datetime(2012, 1, 4)),
                              (18, dt.datetime(2012, 1, 5))]

    actual_max_attr_data = report_calculator.get_month_attr_values(month_data, "Max TemperatureC")
    actual_min_attr_data = report_calculator.get_month_attr_values(month_data, "Min TemperatureC")

    assert actual_max_attr_data == expected_max_attr_data
    assert actual_min_attr_data == expected_min_attr_data


def test_get_attr_values():
    """ Tests "get_attr_values" 
    """

    # Expected 2012, month 3  Min Temperature
    expected_month_3_min = [(20, dt.datetime(2012, 3, 2)),
                            (5, dt.datetime(2012, 3, 3)),
                            (11, dt.datetime(2012, 3, 4)),
                            (18, dt.datetime(2012, 3, 5))]
    # Expected 2012, month 4  Min Temperature
    expected_month_4_min = [(19, dt.datetime(2012, 4, 2)),
                            (16, dt.datetime(2012, 4, 5)),
                            (13, dt.datetime(2012, 4, 7)),
                            (5, dt.datetime(2012, 4, 10))]
    # Expected 2012, year  Min Temperature
    expected_year_2012_min = [(20, dt.datetime(2012, 3, 2)),
                              (5, dt.datetime(2012, 3, 3)),
                              (11, dt.datetime(2012, 3, 4)),
                              (18, dt.datetime(2012, 3, 5)),
                              (19, dt.datetime(2012, 4, 2)),
                              (16, dt.datetime(2012, 4, 5)),
                              (13, dt.datetime(2012, 4, 7)),
                              (5, dt.datetime(2012, 4, 10))]
    # Expected 2012, year  Min Temperature
    expected_year_2012_max = [(12, dt.datetime(2012, 3, 2)),
                              (30, dt.datetime(2012, 3, 3)),
                              (57, dt.datetime(2012, 3, 4)),
                              (40, dt.datetime(2012, 3, 5)),
                              (20, dt.datetime(2012, 4, 2)),
                              (22, dt.datetime(2012, 4, 5)),
                              (25, dt.datetime(2012, 4, 7)),
                              (16, dt.datetime(2012, 4, 10))]

    # Getting Actual values of get_attr_values
    actual_month_3_min = report_calculator.get_attr_values(weather_dataset, "Min TemperatureC", year=2012, month=3)
    actual_month_4_min = report_calculator.get_attr_values(weather_dataset, "Min TemperatureC", year=2012, month=4)
    actual_year_2012_min = report_calculator.get_attr_values(weather_dataset, "Min TemperatureC", year=2012)
    actual_year_2012_max = report_calculator.get_attr_values(weather_dataset, "Max TemperatureC", year=2012)

    assert actual_month_3_min == expected_month_3_min
    assert actual_month_4_min == expected_month_4_min
    assert actual_year_2012_min == expected_year_2012_min
    assert actual_year_2012_max == expected_year_2012_max


def test_get_value():
    """Test 'get_value'
    """

    # Expected Values
    expected_2012_max = (57, dt.datetime(2012, 3, 4))
    expected_2014_max = (510, dt.datetime(2014, 6, 4))
    expected_2014_min = (20, dt.datetime(2014, 6, 2))
    expected_2014_month_7_min = (110, dt.datetime(2014, 7, 2))

    # Actual Values
    actual_2012_max = report_calculator.get_value(weather_dataset, "Max TemperatureC", "max", year=2012)
    actual_2014_max = report_calculator.get_value(weather_dataset, "Max TemperatureC", "max", year=2014)
    actual_2014_min = report_calculator.get_value(weather_dataset, "Min TemperatureC", "min", year=2014)
    actual_2014_month_7_min = report_calculator.get_value(weather_dataset, "Min TemperatureC", "min", year=2014, month=7)

    assert expected_2012_max == actual_2012_max
    assert expected_2014_max == actual_2014_max
    assert expected_2014_min == actual_2014_min
    assert expected_2014_month_7_min == actual_2014_month_7_min


def test_get_mean_attr():
    """Test 'get_mean_attr'
    """

    # Expected Values
    max_mean_2012 = statistics.mean([12,30,57,40,20,22,25,16])
    expected_2012_max = (max_mean_2012, dt.datetime(2012, 3, 2))

    max_mean_2014 = statistics.mean([102,100,510,410,210,210,105,106])
    expected_2014_max = (max_mean_2014, dt.datetime(2014, 6, 2))

    min_mean_2014 = statistics.mean([20,25,101,110,110,111,122,120])
    expected_2014_min = (min_mean_2014, dt.datetime(2014, 6, 2))

    min_mean_2014_month_7 = statistics.mean([110,111,122,120])
    expected_2014_month_7_min = (min_mean_2014_month_7, dt.datetime(2014, 7, 2))

    # Actual Values
    actual_2012_max = report_calculator.get_mean_attr(weather_dataset, "Max TemperatureC", year=2012)
    actual_2014_max = report_calculator.get_mean_attr(weather_dataset, "Max TemperatureC", year=2014)
    actual_2014_min = report_calculator.get_mean_attr(weather_dataset, "Min TemperatureC", year=2014)
    actual_2014_month_7_min = report_calculator.get_mean_attr(weather_dataset, "Min TemperatureC", year=2014, month=7)

    assert expected_2012_max == actual_2012_max
    assert expected_2014_max == actual_2014_max
    assert expected_2014_min == actual_2014_min
    assert expected_2014_month_7_min == actual_2014_month_7_min

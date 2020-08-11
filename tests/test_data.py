import datetime as dt
import statistics

# Test Data
weather_dataset = {2012: {3: [{"PKT": dt.datetime(2012, 3, 2), "Max TemperatureC": 12, "Min TemperatureC": 20},
                              {"PKT": dt.datetime(2012, 3, 3), "Max TemperatureC": 30, "Min TemperatureC": 5},
                              {"PKT": dt.datetime(2012, 3, 4), "Max TemperatureC": 57, "Min TemperatureC": 11},
                              {"PKT": dt.datetime(2012, 3, 5), "Max TemperatureC": None, "Min TemperatureC": 18}],

                          4: [{"PKT": dt.datetime(2012, 4, 2), "Max TemperatureC": 20, "Min TemperatureC": 19},
                              {"PKT": dt.datetime(2012, 4, 5), "Max TemperatureC": 22, "Min TemperatureC": 16},
                              {"PKT": dt.datetime(2012, 4, 7), "Max TemperatureC": 25, "Min TemperatureC": None},
                              {"PKT": dt.datetime(2012, 4, 10), "Max TemperatureC": 16, "Min TemperatureC": 5}]
                          },
                   2014: {6: [{"PKT": dt.datetime(2014, 6, 2), "Max TemperatureC": None, "Min TemperatureC": 20},
                              {"PKT": dt.datetime(2014, 6, 3), "Max TemperatureC": 100, "Min TemperatureC": 25},
                              {"PKT": dt.datetime(2014, 6, 4), "Max TemperatureC": 510, "Min TemperatureC": 101},
                              {"PKT": dt.datetime(2014, 6, 5), "Max TemperatureC": 410, "Min TemperatureC": 110}],

                          7: [{"PKT": dt.datetime(2014, 7, 2), "Max TemperatureC": 210, "Min TemperatureC": 110},
                              {"PKT": dt.datetime(2014, 7, 5), "Max TemperatureC": 210, "Min TemperatureC": None},
                              {"PKT": dt.datetime(2014, 7, 7), "Max TemperatureC": 105, "Min TemperatureC": 122},
                              {"PKT": dt.datetime(2014, 7, 10), "Max TemperatureC": 106, "Min TemperatureC": 120}]
                          }
                   }

# Expected min/max values
expected_max_2012 = (57, dt.datetime(2012, 3, 4))
expected_max_2014 = (510, dt.datetime(2014, 6, 4))
expected_min_2014 = (20, dt.datetime(2014, 6, 2))
expected_min_2014_7 = (110, dt.datetime(2014, 7, 2))


# Expected Mean Values
max_mean_2012 = statistics.mean([12, 30, 57, 20, 22, 25, 16])
expected_max_mean_2012 = (max_mean_2012, dt.datetime(2012, 3, 2))

max_mean_2014 = statistics.mean([100, 510, 410, 210, 210, 105, 106])
expected_max_mean_2014 = (max_mean_2014, dt.datetime(2014, 6, 3))

min_mean_2014 = statistics.mean([20, 25, 101, 110, 110, 122, 120])
expected_min_mean_2014 = (min_mean_2014, dt.datetime(2014, 6, 2))

min_mean_2014_7 = statistics.mean([110, 122, 120])
expected_min_mean_2014_7 = (min_mean_2014_7, dt.datetime(2014, 7, 2))


# Expected Columns values
# Expected 2012, month 3  Max Temperature
expected_max_col_2012_3 = [(12, dt.datetime(2012, 3, 2)),
                           (30, dt.datetime(2012, 3, 3)),
                           (57, dt.datetime(2012, 3, 4))]
# Expected 2012, month 3  Min Temperature
expected_min_col_2012_3 = [(20, dt.datetime(2012, 3, 2)),
                           (5, dt.datetime(2012, 3, 3)),
                           (11, dt.datetime(2012, 3, 4)),
                           (18, dt.datetime(2012, 3, 5))]

# Expected 2012, month 4  Min Temperature
expected_min_col_2012_4 = [(19, dt.datetime(2012, 4, 2)),
                           (16, dt.datetime(2012, 4, 5)),
                           (5, dt.datetime(2012, 4, 10))]

# Expected 2012, year  Min Temperature
expected_min_col_2012 = [(20, dt.datetime(2012, 3, 2)),
                         (5, dt.datetime(2012, 3, 3)),
                         (11, dt.datetime(2012, 3, 4)),
                         (18, dt.datetime(2012, 3, 5)),
                         (19, dt.datetime(2012, 4, 2)),
                         (16, dt.datetime(2012, 4, 5)),
                         (5, dt.datetime(2012, 4, 10))]

# Expected 2012, year  Min Temperature
expected_max_col_2012 = [(12, dt.datetime(2012, 3, 2)),
                         (30, dt.datetime(2012, 3, 3)),
                         (57, dt.datetime(2012, 3, 4)),
                         (20, dt.datetime(2012, 4, 2)),
                         (22, dt.datetime(2012, 4, 5)),
                         (25, dt.datetime(2012, 4, 7)),
                         (16, dt.datetime(2012, 4, 10))]

import datetime as dt


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

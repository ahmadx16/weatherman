import statistics
from operator import itemgetter


class ReportCalculator:

    def __init__(self, weather_dataset):
        """initialize with weather_dataset"""
        self.weather_dataset = weather_dataset

    def get_month_attr_values(self, month_data, attr):
        """Returns readings of a given attribute on given month"""

        month_attr_values = [(day_data[attr],
                              day_data[list(day_data.keys())[0]])
                             for day_data in month_data
                             if day_data[attr] is not None]
        return month_attr_values

    def get_attr_values(self, attr, year, month=-1):
        """Returns readings of a given attribute on given year/month"""

        attr_values = []
        year_data = self.weather_dataset[year]
        if month == -1:
            for month in year_data:
                attr_values.extend(self.get_month_attr_values(year_data[month], attr))
        else:
            attr_values = self.get_month_attr_values(year_data[month], attr)

        return attr_values

    def get_value(self, attr, value_type, year, month=-1):
        """calculates the provided value on given year and month"""

        attr_values = self.get_attr_values(attr, year, month)
        limit_value_function = min if value_type == "min" else max

        return limit_value_function(attr_values, key=itemgetter(0))

    def get_mean_attr(self, attr, year, month=-1):
        """calculates the mean on provided year and month"""

        attr_values = self.get_attr_values(attr, year, month)
        mean_values = [attr[0] for attr in attr_values]
        mean_value = statistics.mean(mean_values)
        month_date = attr_values[0][1]
        return (mean_value, month_date)

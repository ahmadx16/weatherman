from report_calculator import ReportCalculator


class ReportPrinter(ReportCalculator):
    """Class to print report
    """

    def generate_monthly(self, weather_dataset, arg_date, arg_flag):
        """Generate monthly report or chart based on given arguments
        """

        if self.date_exists(weather_dataset, arg_date.year, arg_date.month):
            if arg_flag == 'a':
                self.month_report(weather_dataset, arg_date.year, arg_date.month)
            elif arg_flag == 'c':
                self.month_chart(weather_dataset, arg_date.year, arg_date.month)
        else:
            report_correct_format(arg_flag)

    def generate_reports(self, weather_dataset, args):
        """ Generates the yearly, monthly reports and charts
        """

        if args.e:
            if self.date_exists(weather_dataset, args.e.year):
                self.year_report(weather_dataset, args.e.year)
            else:
                self.report_correct_format('e')
        if args.a:
            self.generate_monthly(weather_dataset, args.a, 'a')
        if args.c:
            self.generate_monthly(weather_dataset, args.c, 'c')

    def year_report(self, weather_dataset, year):
        """Prints Report of a given year

        The report prints Max Temperature,Min Temperature and
        Min Humidity of a given year.
        """

        max_temp, max_temp_date = super().get_value(weather_dataset, "Max TemperatureC", "max", year)
        min_temp, min_temp_date = super().get_value(weather_dataset, "Min TemperatureC", "min", year)
        min_humid, min_humid_date = super().get_value(weather_dataset, "Min Humidity", "min", year)

        print("-- Year {} Report --".format(year))
        print("Highest: {0}C on {1} {2}".format(max_temp,
                                                max_temp_date.strftime("%B"),
                                                max_temp_date.strftime("%d")
                                                ))

        print("Lowest: {0}C on {1} {2}".format(min_temp,
                                               min_temp_date.strftime("%B"),
                                               min_temp_date.strftime("%d")
                                               ))
        print("Humidity: {0}% on {1} {2}\n".format(min_humid,
                                                   min_humid_date.strftime("%B"),
                                                   min_humid_date.strftime("%d")
                                                   ))

    def month_report(self, weather_dataset, year, month):
        """Prints Report of a given month and year

        It prints 'Highest Average temperature', 'Lowest Average
        Temperature' and Averege Mean Humidity of a given month.
        """

        avg_max_temp, month_date = super().get_mean_attr(weather_dataset, "Max TemperatureC", year, month)
        avg_min_temp, month_date = super().get_mean_attr(weather_dataset, "Min TemperatureC", year, month)
        avg_mean_humid, month_date = super().get_mean_attr(weather_dataset, "Mean Humidity", year, month)

        month_name = month_date.strftime("%B")

        print("-- {} {} Report --".format(month_name, year))
        print("Average Highest: {:.0f}C ".format(round(avg_max_temp, 1)))
        print("Average Lowest: {:.0f}C".format(round(avg_min_temp, 1)))
        print("Average Mean Humidity: {:.0f}% \n".format(round(avg_mean_humid, 1)))

    class Colors:
        """Class for colored text on console 
        """

        BLUE = '\033[94m'
        RED = '\033[91m'
        ENDC = '\033[0m'

    def month_chart(self, weather_dataset, year, month):
        """Prints color charts on console of a given month
        """

        high_temps = super().get_attr_values(weather_dataset, "Max TemperatureC",  year, month)
        low_temps = super().get_attr_values(weather_dataset, "Min TemperatureC", year, month)

        month_name = high_temps[0][1].strftime("%B")

        # Saving max temperature and min temperature in dictionaries
        # key is datetime object
        high_temps = {attr[1]: attr[0] for attr in high_temps}
        low_temps = {attr[1]: attr[0] for attr in low_temps}

        # prints colored chart
        print("{0} {1}".format(month_name, year))
        for k in high_temps:
            # low temp chart
            print(k.strftime("%d"), end=" ")
            for _ in range(low_temps[k]):
                print(self.Colors.BLUE + "+" + self.Colors.ENDC, end="")
            # high temp chart
            for _ in range(high_temps[k]):
                print(self.Colors.RED + "+" + self.Colors.ENDC, end="")

            print("", str(low_temps[k])+"C - ", end="")
            print(str(high_temps[k])+"C", end='\n')

    def report_correct_format(self, arg_flag):
        """Gives user flag error and prints sample correct cases
        """

        print(f"The -{arg_flag} flag is given a date (year or month) that does not exist in data set")
        print_correct_format()

    def date_exists(self, weather_dataset, year, month=-1):
        """Returns True if given month/year exists in weather dataset
        """

        if year not in weather_dataset:
            return False
        if month != -1:
            return month in weather_dataset[year]

        return True

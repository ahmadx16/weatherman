from report_calculator import get_attr_values, get_max_attr,\
    get_min_attr, get_mean_attr


def year_report(weather_dataset, year):
    """Prints Report of a given year

    The report prints Max Temperature,Min Temperature and
    Min Humidity of a given year.
    """

    max_temp, max_temp_date = get_max_attr(
        weather_dataset, "Max TemperatureC", year)

    min_temp, min_temp_date = get_min_attr(
        weather_dataset, "Min TemperatureC", year)

    min_humid, min_humid_date = get_min_attr(
        weather_dataset, "Min Humidity", year)

    print("-- Year {} Report --".format(year))
    print("Highest: {0}C on {1} {2}"
          .format(max_temp,
                  max_temp_date.strftime("%B"),
                  max_temp_date.strftime("%d")
                  ))
    print("Lowest: {0}C on {1} {2}"
          .format(min_temp,
                  min_temp_date.strftime("%B"),
                  min_temp_date.strftime("%d")
                  ))
    print("Humidity: {0}% on {1} {2}\n"
          .format(min_humid,
                  min_humid_date.strftime("%B"),
                  min_humid_date.strftime("%d")
                  ))


def month_report(weather_dataset, year, month):
    """Prints Report of a given month and year

       It prints 'Highest Average temperature', 'Lowest Average
       Temperature' and Averege Mean Humidity of a given month.
    """

    avg_max_temp, month_date = get_mean_attr(
        weather_dataset, "Max TemperatureC", year, month)

    avg_min_temp, month_date = get_mean_attr(
        weather_dataset, "Min TemperatureC", year, month)

    avg_mean_humid, month_date = get_mean_attr(
        weather_dataset, "Mean Humidity", year, month)

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


def month_chart(weather_dataset, year, month):
    """Prints color charts on console of a given month
    """

    high_temps = get_attr_values(
        weather_dataset, "Max TemperatureC",  year, month)

    low_temps = get_attr_values(
        weather_dataset, "Min TemperatureC", year, month)

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
            print(Colors.BLUE + "+" + Colors.ENDC, end="")
        # high temp chart
        for _ in range(high_temps[k]):
            print(Colors.RED + "+" + Colors.ENDC, end="")

        print("", str(low_temps[k])+"C - ", end="")
        print(str(high_temps[k])+"C", end='\n')

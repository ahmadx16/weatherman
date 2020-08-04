import statistics


def get_attr_values(weather_dataset, attr, year, month=-1):
    """Returns readings of a given attribute on given year/month 
    """

    attr_values = []
    if month == -1:
        year_data = weather_dataset[year]
        attr_values = [(day_data[attr],
                        day_data[list(day_data.keys())[0]])
                       for month_data in year_data.values()
                       for day_data in month_data
                       if day_data[attr] is not None]

    else:
        month_data = weather_dataset[year][month]
        attr_values = [(day_data[attr],
                        day_data[list(day_data.keys())[0]])
                       for day_data in month_data
                       if day_data[attr] is not None]
    return attr_values


def get_max_temp(weather_dataset, attr, year, month=-1):
    """Calculates the given calculation on provided year and month
    """

    attr_values = get_attr_values(weather_dataset, attr, year, month)
    max_index = max(range(len(attr_values)),
                    key=attr_values.__getitem__)
    max_value = attr_values[max_index][0]
    max_value_date = attr_values[max_index][1]

    return (max_value, max_value_date)


def get_min_temp(weather_dataset, attr, year, month=-1):
    """calculates the minimum temperature on provided year and month
    """

    attr_values = get_attr_values(weather_dataset, attr, year, month)
    min_index = min(range(len(attr_values)),
                    key=attr_values.__getitem__)
    min_value = attr_values[min_index][0]
    min_value_date = attr_values[min_index][1]

    return (min_value, min_value_date)


def get_mean_temp(weather_dataset, attr, year, month=-1):
    """calculates the mean temperature on provided year and month
    """

    attr_values = get_attr_values(weather_dataset, attr, year, month)
    mean_values = [attr[0] for attr in attr_values]
    mean_value = statistics.mean(mean_values)
    month_date = attr_values[0][1]
    return (mean_value, month_date)

import statistics


def get_month_attr_values(weather_dataset, attr, year, month):
    """Returns readings of a given attribute on given month 
    """

    month_data = weather_dataset[year][month]
    month_attr_values = [(day_data[attr],
                          day_data[list(day_data.keys())[0]])
                         for day_data in month_data
                         if day_data[attr] is not None]
    return month_attr_values


def get_attr_values(weather_dataset, attr, year, month=-1):
    """Returns readings of a given attribute on given year/month 
    """

    attr_values = []
    if month == -1:
        year_data = weather_dataset[year]
        for month in year_data:
            attr_values.extend(get_month_attr_values(weather_dataset, attr, year, month))

    else:
        attr_values = get_month_attr_values(weather_dataset, attr, year, month)

    return attr_values


def get_value(weather_dataset, attr, value_type, year, month=-1):
    """calculates the provided value on given year and month
    """

    attr_values = get_attr_values(weather_dataset, attr, year, month)
    if value_type == "min":
        value_index = min(range(len(attr_values)), key=attr_values.__getitem__)
    elif value_type == "max":
        value_index = max(range(len(attr_values)), key=attr_values.__getitem__)
    value = attr_values[value_index][0]
    value_date = attr_values[value_index][1]

    return (value, value_date)


def get_mean_attr(weather_dataset, attr, year, month=-1):
    """calculates the mean on provided year and month
    """

    attr_values = get_attr_values(weather_dataset, attr, year, month)
    mean_values = [attr[0] for attr in attr_values]
    mean_value = statistics.mean(mean_values)
    month_date = attr_values[0][1]
    return (mean_value, month_date)

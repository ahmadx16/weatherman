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


def get_max_attr(weather_dataset, attr, year, month=-1):
    """Calculates max on given attribute 
    """
    # get required attributes values
    attr_values = get_attr_values(weather_dataset, attr, year, month)
    max_index = max(range(len(attr_values)), key=attr_values.__getitem__)
    max_value = attr_values[max_index][0]
    max_value_date = attr_values[max_index][1]

    return (max_value, max_value_date)


def get_min_attr(weather_dataset, attr, year, month=-1):
    """calculates the minimum on provided year and month
    """

    attr_values = get_attr_values(weather_dataset, attr, year, month)
    min_index = min(range(len(attr_values)), key=attr_values.__getitem__)
    min_value = attr_values[min_index][0]
    min_value_date = attr_values[min_index][1]

    return (min_value, min_value_date)


def get_mean_attr(weather_dataset, attr, year, month=-1):
    """calculates the mean on provided year and month
    """

    attr_values = get_attr_values(weather_dataset, attr, year, month)
    mean_values = [attr[0] for attr in attr_values]
    mean_value = statistics.mean(mean_values)
    month_date = attr_values[0][1]
    return (mean_value, month_date)

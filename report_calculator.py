import statistics


def get_attr_values(weather_dataset, attr, year, month=-1):
    """Returns readings of a given attribute on given year/month

    Args:
        weather_dataset (dict): The main dataset
        attr (string): Name of attribute which needs to be extracted
        year (int): Year whose readings is required
        month (int, optional): Month on which calculation is required.
            Skip to get complete years data. Defaults to -1.

    Returns:
        list(tupple): [(attribute, datetime)] 
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

    Args:
        weather_dataset (dict): The main dataset
        attr (string): The attribute on which calculation requires
        year (int): year in which calculation is required
        month (int, optional): Month on which calculation is required.
            Skip to get complete years data. Defaults to -1.

    Returns:
        (float, datetime): calculation result, date from dataset
    """

    attr_values = get_attr_values(weather_dataset, attr, year, month)
    max_index = max(range(len(attr_values)),
                    key=attr_values.__getitem__)
    max_value = attr_values[max_index][0]
    max_value_date = attr_values[max_index][1]

    return (max_value, max_value_date)


def get_min_temp(weather_dataset, attr, year, month=-1):
    """calculates the minimum temperature on provided year and month

    args:
        weather_dataset (dict): the main dataset
        attr (string): the attribute on which calculation requires
        year (int): year in which calculation is required
        month (int, optional): month on which calculation is required.
            skip to get complete years data. defaults to -1.

    returns:
        (float, datetime): calculation result, date from dataset
    """

    attr_values = get_attr_values(weather_dataset, attr, year, month)
    min_index = min(range(len(attr_values)),
                    key=attr_values.__getitem__)
    min_value = attr_values[min_index][0]
    min_value_date = attr_values[min_index][1]

    return (min_value, min_value_date)


def get_mean_temp(weather_dataset, attr, year, month=-1):
    """calculates the mean temperature on provided year and month

    args:
        weather_dataset (dict): the main dataset
        attr (string): the attribute on which calculation requires
        year (int): year in which calculation is required
        month (int, optional): month on which calculation is required.
            skip to get complete years data. defaults to -1.

    returns:
        (float, datetime): calculation result, date from dataset
    """

    attr_values = get_attr_values(weather_dataset, attr, year, month)
    mean_values = [attr[0] for attr in attr_values]
    mean_value = statistics.mean(mean_values)
    month_date = attr_values[0][1]
    return (mean_value, month_date)

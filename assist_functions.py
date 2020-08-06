
def date_to_int(date):
    """Return integer year and month of given date
    """
    return (int(date.strftime("%Y")), int(date.strftime("%m")))

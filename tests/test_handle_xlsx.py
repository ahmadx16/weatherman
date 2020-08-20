from handle_xlsx import HandleXlsx
from test_data import expected_file_month_data


handle_xlsx = HandleXlsx()


def test_handle_xlsx():
    """Test handle xlsx"""

    # file_data = file_handler.handle_csv("./MockData/", "test_file.txt", delim=",")
    year, month, month_data = handle_xlsx.handle("./tests/MockData/", "test_file.xlsx")
    actual_values = (year,
                     month,
                     month_data
                     )
    expected_values = (2004,
                       7,
                       expected_file_month_data
                       )
    assert actual_values == expected_values

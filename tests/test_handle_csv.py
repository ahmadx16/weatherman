from handle_csv import HandleCsv

from test_data import expected_file_month_data

handle_csv = HandleCsv()


def test_handle_csv():
    """Test handle csv"""

    # file_data = file_handler.handle_csv("./MockData/", "test_file.txt", delim=",")
    year, month, month_data = handle_csv.handle("./tests/MockData/", "test_file.txt")

    actual_values = (year,
                     month,
                     month_data
                     )
    expected_values = (2004,
                       7,
                       expected_file_month_data
                       )
    assert actual_values == expected_values

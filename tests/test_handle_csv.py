from handle_csv import HandleCsv

from test_data import expected_file_month_data

handle_csv = HandleCsv()


def test_handle_csv():
    """Test handle csv"""

    # file_data = file_handler.handle_csv("./MockData/", "test_file.txt", delim=",")
    year, month, month_data = handle_csv.handle("./tests/MockData/", "test_file.txt")

    assert year == 2004
    assert month == 7
    assert month_data == expected_file_month_data

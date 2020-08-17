from handle_xlsx import HandleXlsx
from test_data import expected_file_month_data


handle_xlsx = HandleXlsx()


def test_handle_xlsx():
    """Test handle xlsx"""

    # file_data = file_handler.handle_csv("./MockData/", "test_file.txt", delim=",")
    year, month, month_data = handle_xlsx.handle("./tests/MockData/", "test_file.xlsx")
    assert year == 2004
    assert month == 7
    assert month_data == expected_file_month_data

"""
Contains required configurations.
"""


# pylint: disable=too-few-public-methods
class Config:
    """
    All the basic configurations goes here.
    Ensure all the variable names are capitalized.
    """

    EXCEL_DIR = "files"
    EXCEL_FILE = f"{EXCEL_DIR}/example_time_table.xlsx"
    OUTPUT_DIR = "output"
    TEACHERS_OUTPUT_FILE = f"{OUTPUT_DIR}/teachers_time_table.xlsx"
    CLASS_OUTPUT_FILE = f"{OUTPUT_DIR}/teachers_time_table.xlsx"

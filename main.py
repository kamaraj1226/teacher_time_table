"""
Teacher's Timetable
"""

import sys

# from typing import List, Set, Dict
# import pandas as pd
import teachers_handler
import helpers
import clean_up

# from config import Config


def main():
    """
    Main
    NOTE: All the files inside output directory will be removed every time
    Ensure commmenting out if you need those files
    """
    try:
        helpers.clean_output_dir()
    except PermissionError:
        print("Cant remove files ensure no other process is accessing the file.")
        sys.exit(23)

    df = helpers.get_excel()
    df = clean_up.clean_data(df)

    teachers_handler.write_all_teacher_time_table(df)


if __name__ == "__main__":
    main()

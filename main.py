"""
Teacher's Timetable
"""

import sys
from typing import List, Set, Dict
import re
import pandas as pd

# from helpers import get_excel
import helpers
import clean_up

# from clean_up import clean_data
from config import Config


def get_staff_names(df: pd.DataFrame) -> Set[str]:
    """
    Analyze the data and get all the staff names
    Assuming first two columns will be DAY and PERIOD
    """

    columns = df.columns
    columns = columns[2:]
    staffs = set()

    for column in columns:
        for row in df[column].values:
            if isinstance(row, float):
                continue
            staff = extract_staff_name(row)
            if staff:
                staffs.add(staff)

    return staffs


def extract_staff_name(subject_and_staff: str) -> str:
    """
    In the input string it is expected to receive staff name along with subject name
    EXAMPLE:
        TAMIL (T1)
    This function will extract staff name and return the name.
    On worst case of matching expected to receive an empty string.
    """
    pattern = r"\(([^)]+)\)"
    staff = re.search(pattern, subject_and_staff)
    if staff:
        staff = staff.group(1)
        # Remove tailing spaces if any
        staff = staff.strip()
        return staff
    return ""


def get_day_details(
    df: pd.DataFrame, day: str, _class: None | List[str] = None
) -> pd.DataFrame:
    """
    For the given day return the data.
    Assuming there is a column name DAY
    """
    df = df[df["DAY"].map(lambda x: x == day)]
    if _class:
        df = df[_class]
    else:
        df = df[df.columns.to_list()[2:]]
    return df


def display_day_details(
    df: pd.DataFrame, day: str, _class: None | List[str] = None
) -> None:
    """
    For the given day print data.
    NOTE: all the data is tranposed before printing
    Assuming there is a column name DAY
    """
    df = df[df["DAY"].map(lambda x: x == day)]
    df.index = df["PERIOD"]  # type: ignore
    if _class:
        df = df[_class]
    else:
        df = df[df.columns.to_list()[2:]]
    print(df.T)


def extract_subject_name(subject_and_staff: str) -> str:
    """
    In the input string it is expected to receive staff name along with subject name
    EXAMPLE:
        TAMIL (T1)
    This function will extract subject name and return the name.
    On worst case of matching expected to receive an empty string.
    """
    pos = subject_and_staff.find("(")
    subject = subject_and_staff[:pos]
    subject = subject.strip()
    return subject


def get_staff_time_table(
    df: pd.DataFrame, staff: str, total_period: int = 8
) -> Dict[str, Dict[int, str | None]]:
    """
    For the given staff generate staff time table for a week
    """
    days = (
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
    )

    table_dict: Dict[str, Dict[int, str | None]] = {}

    for day in days:

        day_details = get_day_details(df, day)

        day_details = day_details.to_dict()

        for _class, subjects in day_details.items():
            if not isinstance(_class, str):
                continue

            for idx, subject in enumerate(subjects.values()):

                if not isinstance(subject, str):
                    continue

                _staff = extract_staff_name(subject)
                if not _staff:
                    continue

                if _staff != staff:
                    continue
                table_dict.setdefault(day, {i + 1: None for i in range(total_period)})

                subject = extract_subject_name(subject)
                table_dict[day][idx + 1] = format_class_and_subject(_class, subject)
    return table_dict


def format_class_and_subject(_class: str, subject: str):
    """
    Takes class and subject name
    This function is mostly for wrting into excel file.
    You can customize how the string should look in the excel file here.
    """
    _class = _class.replace("'", "")
    return f"{_class} ({subject})"


def write_teacher_time_table(
    table: Dict[str, Dict[int, str | None]], staff: str
) -> None:
    """
    Given the table dictionary write this to an excel file.
    Given staff name will be a sheetname.
    """
    df = pd.DataFrame.from_dict(table)
    try:
        writer = pd.ExcelWriter(
            Config.OUTPUT_EXCEL_LOCATION, mode="a", engine="openpyxl"
        )
    except FileNotFoundError:
        writer = pd.ExcelWriter(
            Config.OUTPUT_EXCEL_LOCATION, mode="w", engine="openpyxl"
        )

    with writer:
        df.to_excel(excel_writer=writer, sheet_name=staff)


def write_all_teacher_time_table(df: pd.DataFrame, staffs: List[str]):
    """
    Required pandas dataframe and staff list
    for the list of staffs generate staff time table
    """
    staffs.sort()
    for staff in staffs:
        table = get_staff_time_table(df, staff)
        write_teacher_time_table(table, staff)


def main():
    """Main
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
    staffs = list(get_staff_names(df))
    write_all_teacher_time_table(df, staffs)


if __name__ == "__main__":
    main()

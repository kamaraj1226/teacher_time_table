"""
Teachers handler 
will handle all the tasks related to staffs
"""

from typing import Set, Dict
import pandas as pd
import helpers
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
            staff = helpers.extract_staff_name(row)
            if staff:
                staffs.add(staff)

    return staffs


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

        day_details = helpers.get_day_details(df, day)

        day_details = day_details.to_dict()

        for _class, subjects in day_details.items():
            if not isinstance(_class, str):
                continue

            for idx, subject in enumerate(subjects.values()):

                if not isinstance(subject, str):
                    continue

                _staff = helpers.extract_staff_name(subject)
                if not _staff:
                    continue

                if _staff != staff:
                    continue
                table_dict.setdefault(day, {i + 1: None for i in range(total_period)})

                subject = helpers.extract_subject_name(subject)
                table_dict[day][idx + 1] = helpers.format_class_and_subject(
                    _class, subject
                )
    return table_dict


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
            Config.TEACHERS_OUTPUT_FILE, mode="a", engine="openpyxl"
        )
    except FileNotFoundError:
        writer = pd.ExcelWriter(
            Config.TEACHERS_OUTPUT_FILE, mode="w", engine="openpyxl"
        )

    with writer:
        df.to_excel(excel_writer=writer, sheet_name=staff)


def write_all_teacher_time_table(df: pd.DataFrame):
    """
    Required pandas dataframe and staff list
    for the list of staffs generate staff time table
    """
    staffs = list(get_staff_names(df))
    staffs.sort()
    for staff in staffs:
        table = get_staff_time_table(df, staff)
        write_teacher_time_table(table, staff)

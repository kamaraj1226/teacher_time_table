"""
Teacher's Timetable
"""

from typing import List, Set, Dict
import re
from collections import namedtuple
import pandas as pd
from helpers import get_excel
from clean_up import clean_data


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


def get_staff_time_table(df: pd.DataFrame, staff: str, total_period: int = 8) -> dict:
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

    details = namedtuple("details", "handling_class subject")
    table_dict: Dict[str, Dict[int, details | None]] = {}

    for day in days:

        day_details = get_day_details(df, day)

        day_details = day_details.to_dict()

        for _class, subjects in day_details.items():

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
                table_dict[day][idx + 1] = details(_class, subject)
    return table_dict


def main():
    """Main"""
    df = get_excel()
    df = clean_data(df)
    staffs = list(get_staff_names(df))
    table = get_staff_time_table(df, "T2")
    print(table["MONDAY"])


if __name__ == "__main__":
    main()

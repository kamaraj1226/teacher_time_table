"""
Teacher substitution
"""

from typing import List, Set, Dict
import re
from collections import namedtuple
import pandas as pd
from config import Config


def fill_days(df: pd.DataFrame) -> pd.DataFrame:
    """
    DAYS column is not properly filled in original excel
    This function will fill all those row values to appropriate day.
    And returns new pandas Dataframe.
    """
    new_df = df.copy()

    cur_day = None
    for i in range(len(df)):

        if isinstance(new_df.iloc[i]["DAY"], str):
            cur_day = new_df.iloc[i]["DAY"].strip()
        new_df.loc[i, "DAY"] = cur_day

    return new_df


def get_rows_with_all_nan(df: pd.DataFrame) -> List[int]:
    """
    Takes dataframe all look for rows which consist only null values.
    """
    rows_with_null = df.isnull().values.all(axis=1)

    null_rows_index = [i for i, val in enumerate(rows_with_null) if val]
    return null_rows_index


def create_new_datafarme(df: pd.DataFrame, null_rows_index: List[int]) -> pd.DataFrame:
    """
    Function takes data frame and the list of integers to be removed
    It removes all the rows which consists null values.
    """
    column_names = df.columns.to_list()
    data = {}
    for column in column_names:
        current_poped = 0
        coulumn_values = df[column].to_list()

        for null_row in null_rows_index:
            coulumn_values.pop(null_row - current_poped)
            current_poped += 1

        data[column] = coulumn_values

    df = pd.DataFrame.from_dict(data)
    return df


def get_excel() -> pd.DataFrame:
    """
    Read excel and return pandas dataframe
    """
    excel_loc = Config.EXCEL_LOCATION
    df = pd.read_excel(excel_loc, sheet_name="progress", skiprows=[0, 1])
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove all the rows which only have null values.

    If Further cleaning is needed will be implemented here.
    """
    null_rows_index = get_rows_with_all_nan(df)

    column_names = df.columns.to_list()
    column_names[0] = "DAY"
    df.columns = column_names

    df = create_new_datafarme(df, null_rows_index)

    df = fill_days(df)
    return df


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
    # print(f"{day:^50s}")
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

                # print(day, _class, period, staff)
                table_dict.setdefault(day, {i + 1: None for i in range(total_period)})

                subject = extract_subject_name(subject)
                table_dict[day][idx + 1] = details(_class, subject)
    return table_dict


def main():
    """Main"""
    df = get_excel()
    df = clean_data(df)
    staffs = list(get_staff_names(df))
    get_staff_time_table(df, "T2")
    # display_day_details(df, "MONDAY")


if __name__ == "__main__":
    main()

"""
All the generic helper functions goes here
"""

import os
import glob
import re
from typing import List
import pandas as pd
from config import Config


def clean_output_dir():
    """
    clean up output directory
    """
    files = glob.glob(f"{Config.OUTPUT_DIR}/*")
    try:
        for f in files:
            print(f"Removing: {os.path.basename(f)}")
            os.remove(f)
    except PermissionError as exc:
        raise exc


def get_excel() -> pd.DataFrame:
    """
    Read excel and return pandas dataframe
    """
    excel_loc = Config.EXCEL_FILE
    df = pd.read_excel(excel_loc, sheet_name="progress", skiprows=[0, 1])
    return df


def get_rows_with_all_nan(df: pd.DataFrame) -> List[int]:
    """
    Takes dataframe all look for rows which consist only null values.
    """
    rows_with_null = df.isnull().values.all(axis=1)

    null_rows_index = [i for i, val in enumerate(rows_with_null) if val]
    return null_rows_index


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


def format_class_and_subject(_class: str, subject: str):
    """
    Takes class and subject name
    This function is mostly for wrting into excel file.
    You can customize how the string should look in the excel file here.
    """
    _class = _class.replace("'", "")
    return f"{_class} ({subject})"


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

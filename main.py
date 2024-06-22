"""
Teacher substitution
"""

from typing import List, Set
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
    # pylint: disable=import-outside-toplevel
    import re

    columns = df.columns
    columns = columns[2:]
    staffs = set()

    pattern = r"\(([^)]+)\)"

    for column in columns:
        for row in df[column].values:
            if isinstance(row, float):
                continue
            staff = re.search(pattern, row)
            if staff:
                staff = staff.group(1)
                # Remove tailing spaces if any
                staff = staff.strip()
                staffs.add(staff)

    return staffs


def main():
    """Main"""
    df = get_excel()
    df = clean_data(df)
    staffs = get_staff_names(df)
    print(staffs)


if __name__ == "__main__":
    main()

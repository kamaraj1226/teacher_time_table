"""
Clean up the datas like 
Filling missing column
"""

from typing import List
import pandas as pd
from helpers import get_rows_with_all_nan


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

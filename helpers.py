"""
All the generic helper functions goes here
"""

from typing import List
import pandas as pd
from config import Config


def get_excel() -> pd.DataFrame:
    """
    Read excel and return pandas dataframe
    """
    excel_loc = Config.EXCEL_LOCATION
    df = pd.read_excel(excel_loc, sheet_name="progress", skiprows=[0, 1])
    return df


def get_rows_with_all_nan(df: pd.DataFrame) -> List[int]:
    """
    Takes dataframe all look for rows which consist only null values.
    """
    rows_with_null = df.isnull().values.all(axis=1)

    null_rows_index = [i for i, val in enumerate(rows_with_null) if val]
    return null_rows_index

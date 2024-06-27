"""
All the generic helper functions goes here
"""

import os
import glob
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

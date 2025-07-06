from pathlib import Path

import pandas as pd
import xlwings
from rich.console import Console

from app.py_ext import stringify_downloads_path



console_api = Console()


def _close_xlsx(output_filename: str):
    if not Path(output_filename).is_file():
        return
    
    output_book = xlwings.Book(output_filename)
    output_book.close()


def to_excel_df(df: pd.DataFrame, output_filename: str):
    try:
        df.to_excel(
            excel_writer=output_filename,
            index=False,
            engine='xlsxwriter'
        )
    except PermissionError as perr:
        _close_xlsx(output_filename)
        to_excel_df(df, output_filename)


def to_log_excel(df: pd.DataFrame, stem_name: str):
    output_file = stringify_downloads_path(stem_name + '.xlsx')

    to_excel_df(
        df=df,
        output_filename=output_file
    )

    return output_file

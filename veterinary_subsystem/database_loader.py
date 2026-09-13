import pandas as pd


def load_veterinary_database(excel_path):
    """
    Load the veterinary Excel workbook into Python.

    Returns:
        A dictionary where each sheet name maps to a pandas DataFrame.
    """

    workbook = pd.read_excel(
        excel_path,
        sheet_name=None
    )

    return workbook
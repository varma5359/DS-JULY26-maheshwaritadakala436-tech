
"""
Load raw motor insurance datasets from CSV files.

This module checks file availability, loads individual CSV files,
and loads all five related insurance tables.
"""

from pathlib import Path

import pandas as pd


def check_file_exists(file_path):
    """
    Check whether the given file exists.

    Args:
        file_path: Path to the CSV file.

    Returns:
        True if the file exists, otherwise False.
    """
    return Path(file_path).is_file()


def load_table(file_path):
    """
    Load a single CSV file into a pandas DataFrame.

    Args:
        file_path: Path to the CSV file.

    Returns:
        pandas DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file is empty.
    """
    file_path = Path(file_path)

    if not check_file_exists(file_path):
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(
            f"CSV file is empty: {file_path}"
        ) from exc

    return df


def load_all_data(data_dir):
    """
    Load all five raw motor insurance datasets.

    Args:
        data_dir: Directory containing the raw CSV files.

    Returns:
        Dictionary containing five pandas DataFrames:
        customers, policies, vehicles, claims, and payments.

    Raises:
        FileNotFoundError: If a required CSV file is missing.
    """
    data_dir = Path(data_dir)

    required_files = {
        "customers": "customers.csv",
        "policies": "policies.csv",
        "vehicles": "vehicles.csv",
        "claims": "claims.csv",
        "payments": "payments.csv",
    }

    data = {}

    for table_name, file_name in required_files.items():
        file_path = data_dir / file_name
        data[table_name] = load_table(file_path)

        print(
            f"Loaded {table_name}: "
            f"{data[table_name].shape[0]} rows, "
            f"{data[table_name].shape[1]} columns"
        )

    return data


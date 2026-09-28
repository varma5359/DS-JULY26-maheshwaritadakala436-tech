import os
import pandas as pd


def check_file_exists(file_path):
    """Check whether the given file exists."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return True


def load_data(file_path):
    """Load the logistics CSV file into a Pandas DataFrame."""
    check_file_exists(file_path)

    df = pd.read_csv(file_path)

    return df
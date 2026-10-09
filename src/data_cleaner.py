
"""
Clean motor insurance datasets.

This module handles missing values, duplicates, text formatting,
date conversion, numeric validation, business rules, and derived
columns for customers, policies, vehicles, claims, and payments.
"""

from pathlib import Path

import pandas as pd


DATE_COLUMNS = {
    "customers": ["date_of_birth", "registration_date"],
    "policies": ["start_date", "end_date"],
    "vehicles": ["registration_date", "manufacture_date"],
    "claims": ["claim_date", "reported_date", "settlement_date"],
    "payments": ["payment_date"],
}

NUMERIC_COLUMNS = {
    "customers": [],
    "policies": ["premium_amount", "coverage_amount"],
    "vehicles": ["vehicle_value", "vehicle_age"],
    "claims": ["claim_amount", "approved_amount"],
    "payments": ["payment_amount"],
}


def handle_missing_values(data):
    """
    Handle missing values without blindly filling every column.

    Text columns receive 'Unknown' only when appropriate.
    Numeric and date columns remain missing for analysis.
    """
    cleaned_data = {}

    for table_name, df in data.items():
        df = df.copy()

        for column in df.select_dtypes(include=["object", "string"]).columns:
            df[column] = df[column].replace(r"^\s*$", pd.NA, regex=True)

            # Do not replace identifiers or date fields with "Unknown".
            if not column.lower().endswith("_id"):
                if column not in DATE_COLUMNS.get(table_name, []):
                    df[column] = df[column].fillna("Unknown")

        cleaned_data[table_name] = df

    return cleaned_data


def remove_duplicates(data):
    """
    Remove exact duplicate rows from each dataset.

    Returns a dictionary of DataFrames.
    """
    cleaned_data = {}

    for table_name, df in data.items():
        df = df.copy()
        before = len(df)

        df = df.drop_duplicates()

        print(
            f"{table_name}: removed {before - len(df)} duplicate rows"
        )

        cleaned_data[table_name] = df

    return cleaned_data


def clean_text_columns(data):
    """
    Standardize whitespace in text columns.

    This function does not change capitalization or category meaning.
    """
    cleaned_data = {}

    for table_name, df in data.items():
        df = df.copy()

        for column in df.select_dtypes(include=["object", "string"]).columns:
            df[column] = df[column].apply(
                lambda value: (
                    " ".join(value.split())
                    if isinstance(value, str)
                    else value
                )
            )

        cleaned_data[table_name] = df

    return cleaned_data


def clean_date_columns(data):
    """
    Convert known date columns to pandas datetime values.

    Unparseable dates become NaT so they can be investigated.
    """
    cleaned_data = {}

    for table_name, df in data.items():
        df = df.copy()

        for column in DATE_COLUMNS.get(table_name, []):
            if column in df.columns:
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )

        cleaned_data[table_name] = df

    return cleaned_data


def validate_numeric_columns(data):
    """
    Convert configured numeric columns to numeric types.

    Invalid values become NaN instead of silently becoming zero.
    """
    cleaned_data = {}

    for table_name, df in data.items():
        df = df.copy()

        for column in NUMERIC_COLUMNS.get(table_name, []):
            if column in df.columns:
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

        cleaned_data[table_name] = df

    return cleaned_data


def validate_business_rules(data):
    """
    Identify common motor insurance business-rule violations.

    Invalid records are reported, not automatically deleted.
    """
    for table_name, df in data.items():
        print(f"\nBusiness-rule checks: {table_name}")

        if table_name == "policies":
            if {"start_date", "end_date"}.issubset(df.columns):
                invalid = (
                    df["start_date"].notna()
                    & df["end_date"].notna()
                    & (df["end_date"] < df["start_date"])
                )
                print("Policies ending before start:", int(invalid.sum()))

            if "premium_amount" in df.columns:
                invalid = df["premium_amount"] < 0
                print("Negative premiums:", int(invalid.sum()))

            if "coverage_amount" in df.columns:
                invalid = df["coverage_amount"] < 0
                print("Negative coverage:", int(invalid.sum()))

        elif table_name == "claims":
            if "claim_amount" in df.columns:
                invalid = df["claim_amount"] < 0
                print("Negative claim amounts:", int(invalid.sum()))

            if "approved_amount" in df.columns:
                invalid = df["approved_amount"] < 0
                print("Negative approved amounts:", int(invalid.sum()))

        elif table_name == "payments":
            if "payment_amount" in df.columns:
                invalid = df["payment_amount"] < 0
                print("Negative payment amounts:", int(invalid.sum()))

    return data


def create_derived_columns(data):
    """
    Create useful analytical columns when source columns exist.

    Column names are checked before calculations so datasets with
    different schemas can still pass through the pipeline.
    """
    derived_data = {
        table_name: df.copy()
        for table_name, df in data.items()
    }

    customers = derived_data.get("customers")
    if customers is not None and "date_of_birth" in customers.columns:
        today = pd.Timestamp.today().normalize()

        customers["customer_age"] = (
            (today - customers["date_of_birth"]).dt.days / 365.25
        ).round(1)

        customers.loc[
            customers["customer_age"] < 0, "customer_age"
        ] = pd.NA

    policies = derived_data.get("policies")
    if policies is not None:
        if {"start_date", "end_date"}.issubset(policies.columns):
            policies["policy_duration_days"] = (
                policies["end_date"] - policies["start_date"]
            ).dt.days

        if {"start_date", "end_date"}.issubset(policies.columns):
            today = pd.Timestamp.today().normalize()

            policies["policy_active_flag"] = (
                policies["start_date"].le(today)
                & policies["end_date"].ge(today)
            ).astype("boolean")

    vehicles = derived_data.get("vehicles")
    if vehicles is not None and "manufacture_date" in vehicles.columns:
        today = pd.Timestamp.today().normalize()

        vehicles["vehicle_age"] = (
            (today - vehicles["manufacture_date"]).dt.days / 365.25
        ).round(1)

        vehicles.loc[
            vehicles["vehicle_age"] < 0, "vehicle_age"
        ] = pd.NA

    claims = derived_data.get("claims")
    if claims is not None:
        if {"reported_date", "claim_date"}.issubset(claims.columns):
            claims["claim_reporting_days"] = (
                claims["reported_date"] - claims["claim_date"]
            ).dt.days

        if {"settlement_date", "claim_date"}.issubset(claims.columns):
            claims["claim_settlement_days"] = (
                claims["settlement_date"] - claims["claim_date"]
            ).dt.days

    return derived_data


def clean_data(data):
    """
    Run the complete cleaning pipeline in a consistent order.

    Returns the cleaned datasets as a dictionary.
    """
    data = handle_missing_values(data)
    data = remove_duplicates(data)
    data = clean_text_columns(data)
    data = clean_date_columns(data)
    data = validate_numeric_columns(data)
    data = validate_business_rules(data)
    data = create_derived_columns(data)

    return data


def save_cleaned_data(data, output_dir):
    """
    Save cleaned datasets as CSV files.

    Args:
        data: Dictionary of cleaned DataFrames.
        output_dir: Directory where cleaned CSV files are saved.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for table_name, df in data.items():
        output_file = output_dir / f"{table_name}_cleaned.csv"
        df.to_csv(output_file, index=False)

        print(f"Saved: {output_file}")


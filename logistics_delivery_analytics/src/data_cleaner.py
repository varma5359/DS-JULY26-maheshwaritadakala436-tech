import pandas as pd
import numpy as np


def handle_missing_values(df):
    """Handle missing values in the logistics dataset."""
    df = df.copy()

    numeric_columns = [
        "distance_km",
        "quantity",
        "weight_kg",
        "shipping_cost",
        "fuel_cost",
        "warehouse_processing_hours",
        "customer_rating",
        "damage_flag",
        "return_flag"
    ]

    for column in numeric_columns:
        if (
            column in df.columns
            and pd.api.types.is_numeric_dtype(df[column])
        ):
            df[column] = df[column].fillna(
                df[column].median()
            )

    text_columns = [
        "warehouse",
        "origin_city",
        "destination_city",
        "product_category",
        "shipping_mode",
        "delivery_partner",
        "delivery_status"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].fillna("Unknown")

    return df


def remove_duplicates(df):
    """Remove duplicate records from the dataset."""
    df = df.copy()

    df = df.drop_duplicates()

    return df


def clean_text_columns(df):
    """Clean text columns by removing extra spaces."""
    df = df.copy()

    text_columns = df.select_dtypes(
        include="object"
    ).columns

    for column in text_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )

    return df


def clean_date_columns(df):
    """Convert date columns to datetime format."""
    df = df.copy()

    date_columns = [
        "order_date",
        "dispatch_date",
        "expected_delivery_date",
        "actual_delivery_date"
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df


def validate_numeric_columns(df):
    """Convert required numeric columns to numeric data types."""
    df = df.copy()

    numeric_columns = [
        "distance_km",
        "quantity",
        "weight_kg",
        "shipping_cost",
        "fuel_cost",
        "warehouse_processing_hours",
        "customer_rating"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


def validate_business_rules(df):
    """Validate and standardize business rules for logistics data."""
    df = df.copy()

    # Convert Yes/No flags to 1/0
    flag_columns = [
        "damage_flag",
        "return_flag"
    ]

    for column in flag_columns:
        if column in df.columns:

            # Convert values to clean lowercase text first
            values = (
                df[column]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            # Convert Yes/No to 1/0
            df[column] = values.map({
                "yes": 1,
                "no": 0,
                "1": 1,
                "0": 0
            })

    # Validate distance
    if "distance_km" in df.columns:
        df.loc[
            df["distance_km"] < 0,
            "distance_km"
        ] = np.nan

    # Validate quantity
    if "quantity" in df.columns:
        df.loc[
            df["quantity"] < 0,
            "quantity"
        ] = np.nan

    # Validate weight
    if "weight_kg" in df.columns:
        df.loc[
            df["weight_kg"] < 0,
            "weight_kg"
        ] = np.nan

    # Validate shipping cost
    if "shipping_cost" in df.columns:
        df.loc[
            df["shipping_cost"] < 0,
            "shipping_cost"
        ] = np.nan

    # Validate fuel cost
    if "fuel_cost" in df.columns:
        df.loc[
            df["fuel_cost"] < 0,
            "fuel_cost"
        ] = np.nan

    # Validate warehouse processing hours
    if "warehouse_processing_hours" in df.columns:
        df.loc[
            df["warehouse_processing_hours"] < 0,
            "warehouse_processing_hours"
        ] = np.nan

    # Validate customer rating
    if "customer_rating" in df.columns:
        df.loc[
            (df["customer_rating"] < 0)
            | (df["customer_rating"] > 5),
            "customer_rating"
        ] = np.nan

    return df


def create_derived_columns(df):
    """Create required logistics business metrics."""
    df = df.copy()

    # Delivery days
    df["delivery_days"] = (
        df["actual_delivery_date"]
        - df["dispatch_date"]
    ).dt.days

    # Delay days
    df["delay_days"] = (
        df["actual_delivery_date"]
        - df["expected_delivery_date"]
    ).dt.days

    # Cost per kilometer
    df["cost_per_km"] = np.where(
        df["distance_km"] > 0,
        df["shipping_cost"] / df["distance_km"],
        0
    )

    # Total logistics cost
    df["total_logistics_cost"] = (
        df["shipping_cost"]
        + df["fuel_cost"]
    )

    # On-time flag
    df["on_time_flag"] = np.where(
        df["delay_days"] <= 0,
        1,
        0
    )

    return df


def clean_data(df):
    """Run the complete logistics data cleaning pipeline."""

    # Step 1: Handle missing values
    df = handle_missing_values(df)

    # Step 2: Remove duplicate rows
    df = remove_duplicates(df)

    # Step 3: Clean text columns
    df = clean_text_columns(df)

    # Step 4: Clean date columns
    df = clean_date_columns(df)

    # Step 5: Validate numeric columns
    df = validate_numeric_columns(df)

    # Step 6: Validate business rules
    df = validate_business_rules(df)

    # Step 7: Handle missing values created during validation
    df = handle_missing_values(df)

    # Step 8: Create derived columns
    df = create_derived_columns(df)

    return df


def save_cleaned_data(df, output_path):
    """Save the cleaned logistics dataset to a CSV file."""
    df.to_csv(
        output_path,
        index=False
    )
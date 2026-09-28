import pandas as pd

from src.data_loader import load_data
from src.data_cleaner import (
    remove_duplicates,
    create_derived_columns,
    clean_data,
    save_cleaned_data
)

from src.business_analysis import (
    calculate_total_orders,
    calculate_on_time_percentage,
    calculate_return_rate
)


def create_sample_data():
    """Create a small sample dataset for testing."""

    data = {
        "order_id": [1, 2, 3],
        "customer_id": [101, 102, 103],
        "order_date": pd.to_datetime(
            ["2025-01-01", "2025-01-02", "2025-01-03"]
        ),
        "warehouse": ["WH1", "WH1", "WH2"],
        "origin_city": ["Hyderabad", "Hyderabad", "Mumbai"],
        "destination_city": ["Delhi", "Chennai", "Pune"],
        "distance_km": [500, 600, 150],
        "product_category": ["Electronics", "Clothing", "Food"],
        "quantity": [2, 3, 1],
        "weight_kg": [5, 10, 2],
        "shipping_mode": ["Air", "Road", "Road"],
        "delivery_partner": ["Partner A", "Partner B", "Partner A"],
        "shipping_cost": [1000, 1200, 500],
        "fuel_cost": [200, 250, 100],
        "warehouse_processing_hours": [3, 4, 2],
        "dispatch_date": pd.to_datetime(
            ["2025-01-02", "2025-01-03", "2025-01-04"]
        ),
        "expected_delivery_date": pd.to_datetime(
            ["2025-01-05", "2025-01-06", "2025-01-05"]
        ),
        "actual_delivery_date": pd.to_datetime(
            ["2025-01-05", "2025-01-08", "2025-01-05"]
        ),
        "delivery_status": [
            "Delivered",
            "Delivered",
            "Delivered"
        ],
        "customer_rating": [5, 4, 5],
        "damage_flag": [0, 0, 1],
        "return_flag": [0, 1, 0]
    }

    return pd.DataFrame(data)


def test_load_data(tmp_path):
    """Test whether data can be loaded successfully."""

    df = create_sample_data()

    file_path = tmp_path / "test_logistics.csv"

    df.to_csv(file_path, index=False)

    loaded_df = load_data(str(file_path))

    assert not loaded_df.empty
    assert len(loaded_df) == 3


def test_remove_duplicates():
    """Test whether duplicate rows are removed."""

    df = create_sample_data()

    duplicate_df = pd.concat(
        [df, df.iloc[[0]]],
        ignore_index=True
    )

    cleaned_df = remove_duplicates(duplicate_df)

    assert len(cleaned_df) == 3


def test_create_derived_columns():
    """Test whether required derived columns are created."""

    df = create_sample_data()

    result = create_derived_columns(df)

    assert "delivery_days" in result.columns
    assert "delay_days" in result.columns
    assert "cost_per_km" in result.columns
    assert "total_logistics_cost" in result.columns
    assert "on_time_flag" in result.columns

    assert result.loc[0, "delivery_days"] == 3
    assert result.loc[0, "delay_days"] == 0
    assert result.loc[1, "delay_days"] == 2
    assert result.loc[0, "on_time_flag"] == 1
    assert result.loc[1, "on_time_flag"] == 0


def test_clean_data():
    """Test the complete data cleaning process."""

    df = create_sample_data()

    cleaned_df = clean_data(df)

    assert not cleaned_df.empty
    assert "delivery_days" in cleaned_df.columns
    assert "delay_days" in cleaned_df.columns
    assert "cost_per_km" in cleaned_df.columns
    assert "total_logistics_cost" in cleaned_df.columns
    assert "on_time_flag" in cleaned_df.columns


def test_clean_data_converts_text_flags():
    """Test text flags are normalized before missing values are filled."""

    df = create_sample_data()
    df["return_flag"] = ["No", "Yes", "No"]
    df["damage_flag"] = ["No", "No", "Yes"]

    cleaned_df = clean_data(df)

    assert cleaned_df["return_flag"].tolist() == [0, 1, 0]
    assert cleaned_df["damage_flag"].tolist() == [0, 0, 1]
    assert round(calculate_return_rate(cleaned_df), 2) == 33.33


def test_calculate_total_orders():
    """Test total order calculation."""

    df = create_sample_data()

    df = create_derived_columns(df)

    result = calculate_total_orders(df)

    assert result == 3


def test_calculate_on_time_percentage():
    """Test on-time delivery percentage calculation."""

    df = create_sample_data()

    df = create_derived_columns(df)

    result = calculate_on_time_percentage(df)

    # Two orders are on time out of three
    assert round(result, 2) == 66.67


def test_save_cleaned_data(tmp_path):
    """Test whether cleaned data is saved successfully."""

    df = create_sample_data()

    output_path = tmp_path / "logistics_cleaned.csv"

    save_cleaned_data(
        df,
        str(output_path)
    )

    assert output_path.exists()

    saved_df = pd.read_csv(output_path)

    assert len(saved_df) == 3
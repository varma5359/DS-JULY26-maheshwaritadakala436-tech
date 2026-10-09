
"""Tests for the motor insurance data pipeline."""

import pandas as pd
import pytest

from src.data_loader import check_file_exists, load_table, load_all_data
from src.data_cleaner import clean_data, save_cleaned_data


def create_sample_csvs(directory):
    """Create small sample CSV files for pipeline testing."""
    directory.mkdir(parents=True, exist_ok=True)

    sample_data = {
        "customers.csv": pd.DataFrame({
            "customer_id": [1, 2],
            "date_of_birth": ["1990-01-01", "1985-05-10"],
            "name": [" Ravi ", "Anita"],
        }),
        "policies.csv": pd.DataFrame({
            "policy_id": [101, 102],
            "customer_id": [1, 2],
            "vehicle_id": [201, 202],
            "start_date": ["2026-01-01", "2026-02-01"],
            "end_date": ["2027-01-01", "2027-02-01"],
            "premium_amount": [1000, 2000],
            "coverage_amount": [50000, 75000],
            "policy_status": ["Active", "Expired"],
            "policy_type": ["Comprehensive", "Third Party"],
        }),
        "vehicles.csv": pd.DataFrame({
            "vehicle_id": [201, 202],
            "manufacture_date": ["2022-01-01", "2020-01-01"],
            "vehicle_value": [500000, 300000],
        }),
        "claims.csv": pd.DataFrame({
            "claim_id": [301, 302],
            "policy_id": [101, 102],
            "customer_id": [1, 2],
            "claim_date": ["2026-03-01", "2026-04-01"],
            "reported_date": ["2026-03-02", "2026-04-02"],
            "settlement_date": ["2026-03-10", "2026-04-15"],
            "claim_amount": [5000, 10000],
            "approved_amount": [4500, 8000],
            "claim_status": ["Approved", "Rejected"],
            "claim_type": ["Accident", "Theft"],
        }),
        "payments.csv": pd.DataFrame({
            "payment_id": [401, 402],
            "claim_id": [301, 302],
            "policy_id": [101, 102],
            "payment_date": ["2026-03-11", "2026-04-16"],
            "payment_amount": [4500, 0],
            "payment_status": ["Paid", "Rejected"],
        }),
    }

    for filename, df in sample_data.items():
        df.to_csv(directory / filename, index=False)


def test_check_file_exists(tmp_path):
    """Check that existing and missing files are detected."""
    file_path = tmp_path / "sample.csv"
    file_path.write_text("id\n1\n", encoding="utf-8")

    assert check_file_exists(file_path) is True
    assert check_file_exists(tmp_path / "missing.csv") is False


def test_load_table(tmp_path):
    """Check that a CSV is loaded into a DataFrame."""
    file_path = tmp_path / "sample.csv"
    pd.DataFrame({"id": [1, 2]}).to_csv(file_path, index=False)

    df = load_table(file_path)

    assert len(df) == 2
    assert list(df.columns) == ["id"]


def test_load_table_missing_file(tmp_path):
    """Check that loading a missing CSV raises an error."""
    with pytest.raises(FileNotFoundError):
        load_table(tmp_path / "missing.csv")


def test_load_all_data(tmp_path):
    """Check that all five insurance tables are loaded."""
    create_sample_csvs(tmp_path)

    data = load_all_data(tmp_path)

    assert set(data.keys()) == {
        "customers", "policies", "vehicles", "claims", "payments"
    }
    assert len(data["customers"]) == 2
    assert len(data["policies"]) == 2


def test_clean_data_and_save(tmp_path):
    """Check that cleaning and exporting datasets work."""
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "cleaned"

    create_sample_csvs(raw_dir)
    raw_data = load_all_data(raw_dir)

    cleaned_data = clean_data(raw_data)
    save_cleaned_data(cleaned_data, output_dir)

    assert (output_dir / "customers_cleaned.csv").exists()
    assert (output_dir / "policies_cleaned.csv").exists()
    assert (output_dir / "vehicles_cleaned.csv").exists()
    assert (output_dir / "claims_cleaned.csv").exists()
    assert (output_dir / "payments_cleaned.csv").exists()

    customers = pd.read_csv(output_dir / "customers_cleaned.csv")
    assert "customer_age" in customers.columns

    policies = pd.read_csv(output_dir / "policies_cleaned.csv")
    assert "policy_duration_days" in policies.columns


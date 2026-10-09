
"""Tests for motor insurance dataset validation."""

import pandas as pd

from src.validation import (
    validate_customers,
    validate_vehicles,
    validate_policies,
    validate_claims,
    validate_payments,
    validate_relationships,
    validate_all_tables,
)


def valid_data():
    """Return five related datasets with valid IDs and relationships."""
    return {
        "customers": pd.DataFrame({
            "customer_id": [1, 2],
        }),
        "vehicles": pd.DataFrame({
            "vehicle_id": [201, 202],
        }),
        "policies": pd.DataFrame({
            "policy_id": [101, 102],
            "customer_id": [1, 2],
            "vehicle_id": [201, 202],
        }),
        "claims": pd.DataFrame({
            "claim_id": [301, 302],
            "policy_id": [101, 102],
            "customer_id": [1, 2],
        }),
        "payments": pd.DataFrame({
            "payment_id": [401, 402],
            "claim_id": [301, 302],
            "policy_id": [101, 102],
        }),
    }


def test_validate_customers_success():
    """Check that valid customer IDs pass validation."""
    df = pd.DataFrame({"customer_id": [1, 2, 3]})

    assert validate_customers(df) == []


def test_validate_customers_duplicate_ids():
    """Check that duplicate customer IDs are reported."""
    df = pd.DataFrame({"customer_id": [1, 1, 2]})

    errors = validate_customers(df)

    assert any("duplicate" in error.lower() for error in errors)


def test_validate_customers_missing_ids():
    """Check that missing customer IDs are reported."""
    df = pd.DataFrame({"customer_id": [1, None, 3]})

    errors = validate_customers(df)

    assert any("missing values" in error.lower() for error in errors)


def test_validate_vehicles_success():
    """Check valid vehicle IDs."""
    df = pd.DataFrame({"vehicle_id": [201, 202]})

    assert validate_vehicles(df) == []


def test_validate_policies_success():
    """Check that policies contain the required columns and unique IDs."""
    df = pd.DataFrame({
        "policy_id": [101, 102],
        "customer_id": [1, 2],
        "vehicle_id": [201, 202],
    })

    assert validate_policies(df) == []


def test_validate_claims_success():
    """Check that claims contain required columns and unique IDs."""
    df = pd.DataFrame({
        "claim_id": [301],
        "policy_id": [101],
        "customer_id": [1],
    })

    assert validate_claims(df) == []


def test_validate_payments_success():
    """Check that payments contain required columns and unique IDs."""
    df = pd.DataFrame({
        "payment_id": [401],
        "claim_id": [301],
        "policy_id": [101],
    })

    assert validate_payments(df) == []


def test_missing_required_column():
    """Check that missing required columns are reported."""
    df = pd.DataFrame({"name": ["Ravi"]})

    errors = validate_customers(df)

    assert any("missing required columns" in error for error in errors)


def test_validate_relationships_success():
    """Check that valid foreign-key relationships pass."""
    data = valid_data()

    assert validate_relationships(data) == []


def test_validate_relationships_invalid_customer():
    """Check that an unknown customer reference is reported."""
    data = valid_data()
    data["policies"].loc[0, "customer_id"] = 999

    errors = validate_relationships(data)

    assert any("no matching" in error for error in errors)


def test_validate_relationships_missing_foreign_key():
    """Check that a missing foreign key is reported."""
    data = valid_data()
    data["claims"].loc[0, "policy_id"] = None

    errors = validate_relationships(data)

    assert any("missing foreign-key values" in error for error in errors)


def test_validate_all_tables_success():
    """Check that the complete valid dataset passes validation."""
    data = valid_data()

    assert validate_all_tables(data) == []


def test_validate_all_tables_missing_dataset():
    """Check that a missing dataset is reported."""
    data = valid_data()
    del data["payments"]

    errors = validate_all_tables(data)

    assert any("Missing dataset: payments" in error for error in errors)



"""Tests for motor insurance business KPI calculations."""

import pandas as pd
import pytest

from src.insurance_analysis import (
    analyze_policies,
    analyze_premiums,
    analyze_claims,
    analyze_settlement,
    analyze_risk_ratios,
    analyze_customers,
    analyze_vehicles,
    analyze_business,
)


@pytest.fixture
def sample_data():
    """Provide predictable insurance data for KPI tests."""
    return {
        "customers": pd.DataFrame({
            "customer_id": [1, 2],
            "customer_age": [30, 40],
        }),
        "policies": pd.DataFrame({
            "policy_id": [101, 102, 103],
            "policy_status": ["Active", "Active", "Expired"],
            "premium_amount": [100, 200, 700],
            "coverage_amount": [1000, 2000, 3000],
        }),
        "vehicles": pd.DataFrame({
            "vehicle_id": [201, 202],
            "vehicle_age": [3, 5],
            "vehicle_value": [500000, 300000],
        }),
        "claims": pd.DataFrame({
            "claim_id": [301, 302, 303, 304],
            "claim_amount": [100, 200, 300, 400],
            "claim_status": [
                "Approved", "Rejected", "Settled", "Pending"
            ],
            "claim_settlement_days": [5, 10, 15, None],
        }),
        "payments": pd.DataFrame({
            "payment_id": [401, 402],
            "payment_amount": [100, 150],
        }),
    }


def test_analyze_policies(sample_data):
    """Check total and active policy calculations."""
    result = analyze_policies(sample_data)

    assert result["total_policies"] == 3
    assert result["active_policies"] == 2
    assert result["inactive_policies"] == 1
    assert result["active_policy_rate"] == pytest.approx(66.67)


def test_analyze_premiums(sample_data):
    """Check premium totals and averages."""
    result = analyze_premiums(sample_data)

    assert result["total_premium"] == 1000
    assert result["average_premium"] == pytest.approx(1000 / 3)
    assert result["median_premium"] == 200


def test_analyze_claims(sample_data):
    """Check claim counts, amounts, and status rates."""
    result = analyze_claims(sample_data)

    assert result["total_claims"] == 4
    assert result["total_claim_amount"] == 1000
    assert result["average_claim_amount"] == 250
    assert result["approved_claims"] == 2
    assert result["rejected_claims"] == 1
    assert result["claim_approval_rate"] == 50
    assert result["claim_rejection_rate"] == 25


def test_analyze_settlement(sample_data):
    """Check that missing settlement durations are excluded."""
    result = analyze_settlement(sample_data)

    assert result["average_settlement_days"] == 10


def test_analyze_risk_ratios(sample_data):
    """Check claim-to-premium and payment-to-claim ratios."""
    result = analyze_risk_ratios(sample_data)

    assert result["claim_to_premium_ratio"] == 100
    assert result["paid_claim_ratio"] == 25
    assert result["total_payment_amount"] == 250


def test_analyze_customers(sample_data):
    """Check customer counts and average age."""
    result = analyze_customers(sample_data)

    assert result["total_customers"] == 2
    assert result["average_customer_age"] == 35


def test_analyze_vehicles(sample_data):
    """Check vehicle counts, ages, and values."""
    result = analyze_vehicles(sample_data)

    assert result["total_vehicles"] == 2
    assert result["average_vehicle_age"] == 4
    assert result["average_vehicle_value"] == 400000


def test_analyze_business(sample_data):
    """Check that the combined KPI summary includes each section."""
    result = analyze_business(sample_data)

    assert result["total_policies"] == 3
    assert result["total_premium"] == 1000
    assert result["total_claims"] == 4
    assert result["total_customers"] == 2
    assert result["total_vehicles"] == 2


def test_empty_data():
    """Check that KPI functions handle empty datasets."""
    data = {
        "customers": pd.DataFrame(),
        "policies": pd.DataFrame(),
        "vehicles": pd.DataFrame(),
        "claims": pd.DataFrame(),
        "payments": pd.DataFrame(),
    }

    result = analyze_business(data)

    assert result["total_policies"] == 0
    assert result["total_premium"] == 0
    assert result["total_claims"] == 0
    assert result["total_customers"] == 0
    assert result["total_vehicles"] == 0


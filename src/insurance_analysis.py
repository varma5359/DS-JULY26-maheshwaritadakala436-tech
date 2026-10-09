
"""
Motor Insurance Analytics.

Calculate policy, premium, claim, settlement, customer, vehicle,
and risk-related business KPIs from the insurance datasets.
"""

import pandas as pd


def get_numeric_series(df, column):
    """Return a numeric Series, or an empty Series if unavailable."""
    if column not in df.columns:
        return pd.Series(dtype="float64")

    return pd.to_numeric(df[column], errors="coerce")


def get_status_series(df, column):
    """Return normalized lowercase status values."""
    if column not in df.columns:
        return pd.Series("", index=df.index, dtype="string")

    return df[column].astype("string").str.strip().str.lower().fillna("")


def calculate_rate(numerator, denominator):
    """Calculate a percentage safely when the denominator is nonzero."""
    if denominator == 0:
        return 0.0

    return round((numerator / denominator) * 100, 2)


def analyze_policies(data):
    """Calculate total, active, and inactive policy KPIs."""
    policies = data.get("policies", pd.DataFrame())

    if policies.empty:
        return {
            "total_policies": 0,
            "active_policies": 0,
            "inactive_policies": 0,
            "active_policy_rate": 0.0,
        }

    total = (
        policies["policy_id"].nunique()
        if "policy_id" in policies.columns
        else len(policies)
    )

    if "policy_status" in policies.columns:
        status = get_status_series(policies, "policy_status")
        active = int(status.isin(["active", "in force", "in-force"]).sum())
    elif "policy_active_flag" in policies.columns:
        active = int(
            policies["policy_active_flag"].fillna(False).astype(bool).sum()
        )
    else:
        active = 0

    return {
        "total_policies": int(total),
        "active_policies": active,
        "inactive_policies": max(int(total) - active, 0),
        "active_policy_rate": calculate_rate(active, int(total)),
    }


def analyze_premiums(data):
    """Calculate total, average, and median policy premiums."""
    policies = data.get("policies", pd.DataFrame())
    premiums = get_numeric_series(policies, "premium_amount").dropna()

    if premiums.empty:
        return {
            "total_premium": 0.0,
            "average_premium": 0.0,
            "median_premium": 0.0,
        }

    return {
        "total_premium": round(float(premiums.sum()), 2),
        "average_premium": float(premiums.mean()),
        "median_premium": round(float(premiums.median()), 2),
    }


def analyze_claims(data):
    """Calculate claim counts, amounts, and approval/rejection rates."""
    claims = data.get("claims", pd.DataFrame())

    if claims.empty:
        return {
            "total_claims": 0,
            "total_claim_amount": 0.0,
            "average_claim_amount": 0.0,
            "approved_claims": 0,
            "rejected_claims": 0,
            "claim_approval_rate": 0.0,
            "claim_rejection_rate": 0.0,
        }

    total_claims = (
        claims["claim_id"].nunique()
        if "claim_id" in claims.columns
        else len(claims)
    )

    amounts = get_numeric_series(claims, "claim_amount").dropna()

    if "claim_status" in claims.columns:
        status = get_status_series(claims, "claim_status")
        approved = int(status.isin(["approved", "settled", "paid"]).sum())
        rejected = int(status.isin(["rejected", "declined"]).sum())
    else:
        approved = 0
        rejected = 0

    return {
        "total_claims": int(total_claims),
        "total_claim_amount": round(float(amounts.sum()), 2),
        "average_claim_amount": (
            round(float(amounts.mean()), 2) if not amounts.empty else 0.0
        ),
        "approved_claims": approved,
        "rejected_claims": rejected,
        "claim_approval_rate": calculate_rate(approved, int(total_claims)),
        "claim_rejection_rate": calculate_rate(rejected, int(total_claims)),
    }


def analyze_settlement(data):
    """Calculate average claim settlement time in days."""
    claims = data.get("claims", pd.DataFrame())

    if claims.empty:
        return {"average_settlement_days": 0.0}

    if "claim_settlement_days" in claims.columns:
        days = get_numeric_series(
            claims, "claim_settlement_days"
        ).dropna()
    elif {"claim_date", "settlement_date"}.issubset(claims.columns):
        claim_dates = pd.to_datetime(
            claims["claim_date"], errors="coerce"
        )
        settlement_dates = pd.to_datetime(
            claims["settlement_date"], errors="coerce"
        )
        days = (settlement_dates - claim_dates).dt.days.dropna()
    else:
        return {"average_settlement_days": 0.0}

    days = days[days >= 0]

    return {
        "average_settlement_days": (
            round(float(days.mean()), 2) if not days.empty else 0.0
        )
    }


def analyze_risk_ratios(data):
    """Calculate claim-to-premium and paid-claim ratios as percentages."""
    policies = data.get("policies", pd.DataFrame())
    claims = data.get("claims", pd.DataFrame())
    payments = data.get("payments", pd.DataFrame())

    total_premium = float(
        get_numeric_series(policies, "premium_amount").dropna().sum()
    )
    total_claim_amount = float(
        get_numeric_series(claims, "claim_amount").dropna().sum()
    )
    total_payments = float(
        get_numeric_series(payments, "payment_amount").dropna().sum()
    )

    return {
        "claim_to_premium_ratio": calculate_rate(
            total_claim_amount, total_premium
        ),
        "paid_claim_ratio": calculate_rate(
            total_payments, total_claim_amount
        ),
        "total_payment_amount": round(total_payments, 2),
    }


def analyze_customers(data):
    """Calculate customer counts and average customer age."""
    customers = data.get("customers", pd.DataFrame())

    if customers.empty:
        return {
            "total_customers": 0,
            "average_customer_age": 0.0,
        }

    total = (
        customers["customer_id"].nunique()
        if "customer_id" in customers.columns
        else len(customers)
    )

    ages = get_numeric_series(customers, "customer_age").dropna()
    ages = ages[ages >= 0]

    return {
        "total_customers": int(total),
        "average_customer_age": (
            round(float(ages.mean()), 1) if not ages.empty else 0.0
        ),
    }


def analyze_vehicles(data):
    """Calculate vehicle counts, average age, and average value."""
    vehicles = data.get("vehicles", pd.DataFrame())

    if vehicles.empty:
        return {
            "total_vehicles": 0,
            "average_vehicle_age": 0.0,
            "average_vehicle_value": 0.0,
        }

    total = (
        vehicles["vehicle_id"].nunique()
        if "vehicle_id" in vehicles.columns
        else len(vehicles)
    )

    ages = get_numeric_series(vehicles, "vehicle_age").dropna()
    ages = ages[ages >= 0]
    values = get_numeric_series(vehicles, "vehicle_value").dropna()

    return {
        "total_vehicles": int(total),
        "average_vehicle_age": (
            round(float(ages.mean()), 1) if not ages.empty else 0.0
        ),
        "average_vehicle_value": (
            round(float(values.mean()), 2) if not values.empty else 0.0
        ),
    }


def analyze_business(data):
    """Combine the main insurance KPIs into one business summary."""
    summary = {}

    summary.update(analyze_policies(data))
    summary.update(analyze_premiums(data))
    summary.update(analyze_claims(data))
    summary.update(analyze_settlement(data))
    summary.update(analyze_risk_ratios(data))
    summary.update(analyze_customers(data))
    summary.update(analyze_vehicles(data))

    return summary


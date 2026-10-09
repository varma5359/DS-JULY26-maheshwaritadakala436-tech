
"""
Generate business insights and recommendations for motor insurance.

This module analyzes portfolio, claims, premiums, customers, vehicles,
and risk patterns using the cleaned insurance datasets.
"""

import pandas as pd


def generate_portfolio_insights(data):
    """Generate insights about the overall insurance portfolio."""
    insights = []

    policies = data.get("policies", pd.DataFrame())
    customers = data.get("customers", pd.DataFrame())

    if policies.empty:
        return ["No policy data available for portfolio analysis."]

    insights.append(f"Total policies recorded: {len(policies):,}")

    if "policy_id" in policies.columns:
        insights.append(
            f"Unique policies: {policies['policy_id'].nunique():,}"
        )

    if "policy_status" in policies.columns:
        status_counts = policies["policy_status"].value_counts(
            dropna=True
        )

        if not status_counts.empty:
            top_status = status_counts.index[0]
            insights.append(
                f"Most common policy status: {top_status} "
                f"({status_counts.iloc[0]:,} policies)"
            )

    if not customers.empty and "customer_id" in customers.columns:
        insights.append(
            f"Unique customers recorded: "
            f"{customers['customer_id'].nunique():,}"
        )

    return insights


def generate_claim_insights(data):
    """Generate insights about claim frequency and claim amounts."""
    insights = []

    claims = data.get("claims", pd.DataFrame())

    if claims.empty:
        return ["No claim data available for analysis."]

    insights.append(f"Total claim records: {len(claims):,}")

    if "claim_amount" in claims.columns:
        amounts = pd.to_numeric(
            claims["claim_amount"], errors="coerce"
        ).dropna()

        if not amounts.empty:
            insights.append(
                f"Total reported claim amount: {amounts.sum():,.2f}"
            )
            insights.append(
                f"Average reported claim amount: {amounts.mean():,.2f}"
            )
            insights.append(
                f"Highest reported claim amount: {amounts.max():,.2f}"
            )

    if "claim_status" in claims.columns:
        status_counts = claims["claim_status"].value_counts(
            dropna=True
        )

        if not status_counts.empty:
            insights.append(
                f"Most common claim status: {status_counts.index[0]} "
                f"({status_counts.iloc[0]:,} claims)"
            )

    if "claim_type" in claims.columns:
        type_counts = claims["claim_type"].value_counts(dropna=True)

        if not type_counts.empty:
            insights.append(
                f"Most frequent claim type: {type_counts.index[0]} "
                f"({type_counts.iloc[0]:,} claims)"
            )

    return insights


def generate_premium_insights(data):
    """Generate insights about premium income."""
    insights = []

    policies = data.get("policies", pd.DataFrame())

    if policies.empty:
        return ["No policy data available for premium analysis."]

    if "premium_amount" not in policies.columns:
        return ["Premium amount column is unavailable."]

    premiums = pd.to_numeric(
        policies["premium_amount"], errors="coerce"
    ).dropna()

    if premiums.empty:
        return ["No valid premium values available."]

    insights.append(f"Total recorded premium: {premiums.sum():,.2f}")
    insights.append(f"Average premium: {premiums.mean():,.2f}")
    insights.append(f"Median premium: {premiums.median():,.2f}")

    if "policy_type" in policies.columns:
        premium_by_type = policies.assign(
            _premium=pd.to_numeric(
                policies["premium_amount"], errors="coerce"
            )
        ).groupby("policy_type", dropna=True)["_premium"].sum()

        if not premium_by_type.empty:
            top_type = premium_by_type.idxmax()
            insights.append(
                f"Policy type with the highest total premium: "
                f"{top_type} ({premium_by_type.max():,.2f})"
            )

    return insights


def generate_customer_insights(data):
    """Generate insights about customer demographics."""
    insights = []

    customers = data.get("customers", pd.DataFrame())

    if customers.empty:
        return ["No customer data available for analysis."]

    insights.append(f"Total customer records: {len(customers):,}")

    if "customer_id" in customers.columns:
        insights.append(
            f"Unique customers: {customers['customer_id'].nunique():,}"
        )

    if "customer_age" in customers.columns:
        ages = pd.to_numeric(
            customers["customer_age"], errors="coerce"
        ).dropna()

        if not ages.empty:
            insights.append(f"Average customer age: {ages.mean():.1f}")
            insights.append(
                f"Customer age range: {ages.min():.1f} to "
                f"{ages.max():.1f} years"
            )

    if "region" in customers.columns:
        regions = customers["region"].value_counts(dropna=True)

        if not regions.empty:
            insights.append(
                f"Region with the most customer records: "
                f"{regions.index[0]} ({regions.iloc[0]:,})"
            )

    return insights


def generate_vehicle_insights(data):
    """Generate insights about insured vehicles."""
    insights = []

    vehicles = data.get("vehicles", pd.DataFrame())

    if vehicles.empty:
        return ["No vehicle data available for analysis."]

    insights.append(f"Total vehicle records: {len(vehicles):,}")

    if "vehicle_id" in vehicles.columns:
        insights.append(
            f"Unique vehicles: {vehicles['vehicle_id'].nunique():,}"
        )

    if "vehicle_type" in vehicles.columns:
        type_counts = vehicles["vehicle_type"].value_counts(
            dropna=True
        )

        if not type_counts.empty:
            insights.append(
                f"Most common vehicle type: {type_counts.index[0]} "
                f"({type_counts.iloc[0]:,} vehicles)"
            )

    if "vehicle_age" in vehicles.columns:
        ages = pd.to_numeric(
            vehicles["vehicle_age"], errors="coerce"
        ).dropna()

        if not ages.empty:
            insights.append(f"Average vehicle age: {ages.mean():.1f} years")

    if "vehicle_value" in vehicles.columns:
        values = pd.to_numeric(
            vehicles["vehicle_value"], errors="coerce"
        ).dropna()

        if not values.empty:
            insights.append(
                f"Average recorded vehicle value: {values.mean():,.2f}"
            )

    return insights


def generate_risk_patterns(data):
    """Identify descriptive claim patterns by region or vehicle type."""
    insights = []

    claims = data.get("claims", pd.DataFrame())
    vehicles = data.get("vehicles", pd.DataFrame())

    if claims.empty:
        return ["No claim data available for risk-pattern analysis."]

    # Claim frequency by region, when region exists in claims.
    if "region" in claims.columns:
        counts = claims["region"].value_counts(dropna=True)

        if not counts.empty:
            insights.append(
                f"Region with the most recorded claims: "
                f"{counts.index[0]} ({counts.iloc[0]:,} claims)"
            )

    # Claim amounts by vehicle type require a valid vehicle_type
    # column in claims, or a vehicle join using vehicle_id.
    if (
        "vehicle_type" in claims.columns
        and "claim_amount" in claims.columns
    ):
        claim_data = claims.copy()
        claim_data["claim_amount"] = pd.to_numeric(
            claim_data["claim_amount"], errors="coerce"
        )

        grouped = claim_data.groupby(
            "vehicle_type", dropna=True
        )["claim_amount"].mean().dropna()

        if not grouped.empty:
            insights.append(
                f"Vehicle type with the highest average claim amount: "
                f"{grouped.idxmax()} ({grouped.max():,.2f})"
            )

    elif (
        not vehicles.empty
        and {"vehicle_id", "vehicle_type"}.issubset(vehicles.columns)
        and "vehicle_id" in claims.columns
        and "claim_amount" in claims.columns
    ):
        claim_data = claims.copy()
        claim_data["claim_amount"] = pd.to_numeric(
            claim_data["claim_amount"], errors="coerce"
        )

        # Merge vehicle details without changing the source DataFrames.
        merged = claim_data.merge(
            vehicles[["vehicle_id", "vehicle_type"]].drop_duplicates(
                subset=["vehicle_id"]
            ),
            on="vehicle_id",
            how="left",
            validate="many_to_one",
        )

        grouped = merged.groupby(
            "vehicle_type", dropna=True
        )["claim_amount"].mean().dropna()

        if not grouped.empty:
            insights.append(
                f"Vehicle type with the highest average claim amount: "
                f"{grouped.idxmax()} ({grouped.max():,.2f})"
            )

    if not insights:
        insights.append(
            "Insufficient matching columns to identify risk patterns."
        )

    return insights


def generate_business_recommendations(data):
    """Generate preliminary recommendations based on observed patterns."""
    recommendations = []

    policies = data.get("policies", pd.DataFrame())
    claims = data.get("claims", pd.DataFrame())

    if not claims.empty and "claim_status" in claims.columns:
        statuses = claims["claim_status"].astype("string").str.strip().str.lower()
        pending_count = statuses.isin(
            ["pending", "under review", "in progress"]
        ).sum()

        if pending_count:
            recommendations.append(
                f"Review {pending_count:,} claims marked as pending "
                "or in progress to identify processing delays."
            )

    if (
        not policies.empty
        and {"premium_amount", "policy_type"}.issubset(policies.columns)
    ):
        premium_data = policies.copy()
        premium_data["premium_amount"] = pd.to_numeric(
            premium_data["premium_amount"], errors="coerce"
        )

        summary = premium_data.groupby(
            "policy_type", dropna=True
        )["premium_amount"].agg(["count", "mean"])

        if len(summary) > 1:
            recommendations.append(
                "Compare average premiums across policy types and "
                "review differences alongside coverage and claim experience."
            )

    if not claims.empty and "claim_amount" in claims.columns:
        amounts = pd.to_numeric(
            claims["claim_amount"], errors="coerce"
        ).dropna()

        if not amounts.empty:
            threshold = amounts.quantile(0.95)
            high_claims = int((amounts > threshold).sum())

            if high_claims:
                recommendations.append(
                    f"Review {high_claims:,} claims above the "
                    f"95th-percentile claim amount ({threshold:,.2f}) "
                    "for appropriate investigation and validation."
                )

    if not recommendations:
        recommendations.append(
            "Collect and validate policy, premium, claim, and settlement "
            "data before making targeted business recommendations."
        )

    return recommendations


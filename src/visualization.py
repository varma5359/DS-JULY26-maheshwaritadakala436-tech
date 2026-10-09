
"""
Motor Insurance Analytics - Visualization Module.

Creates charts for policy, premium, claim, settlement,
customer, vehicle, regional, and payment analysis.
"""

import logging

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.logger import setup_logger


logger = setup_logger()

sns.set_theme(style="whitegrid")


def get_data(data, table_name):
    """Return a copy of a dataset from the data dictionary."""
    return data.get(table_name, pd.DataFrame()).copy()


def get_column(df, column):
    """Return a column as a Series, or an empty Series if unavailable."""
    if column not in df.columns:
        return pd.Series(dtype="object")

    return df[column]


def numeric_column(df, column):
    """Convert a column to numeric values, coercing invalid values."""
    return pd.to_numeric(get_column(df, column), errors="coerce")


def prepare_chart(title, xlabel, ylabel, figsize=(10, 5)):
    """Create a figure and axis with a consistent chart layout."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig, ax


def finish_chart(fig, ax, rotate_labels=False):
    """Format the chart and return its figure."""
    if rotate_labels:
        ax.tick_params(axis="x", labelrotation=45)

    fig.tight_layout()
    return fig


def plot_policy_status(data):
    """Plot the number of policies by policy status."""
    df = get_data(data, "policies")

    if "policy_status" not in df.columns:
        logger.warning("policy_status column is missing.")
        return None

    counts = df["policy_status"].fillna("Unknown").value_counts()

    fig, ax = prepare_chart(
        "Policy Status Distribution", "Policy Status", "Number of Policies"
    )
    sns.barplot(x=counts.index, y=counts.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_policy_type_distribution(data):
    """Plot the distribution of insurance policy types."""
    df = get_data(data, "policies")

    if "policy_type" not in df.columns:
        logger.warning("policy_type column is missing.")
        return None

    counts = df["policy_type"].fillna("Unknown").value_counts()

    fig, ax = prepare_chart(
        "Policy Type Distribution", "Policy Type", "Number of Policies"
    )
    sns.barplot(x=counts.index, y=counts.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_premium_by_policy_type(data):
    """Plot total premium collected for each policy type."""
    df = get_data(data, "policies")

    if not {"policy_type", "premium_amount"}.issubset(df.columns):
        logger.warning("Required premium analysis columns are missing.")
        return None

    df["premium_amount"] = pd.to_numeric(
        df["premium_amount"], errors="coerce"
    )
    summary = df.groupby("policy_type")["premium_amount"].sum().dropna()

    fig, ax = prepare_chart(
        "Total Premium by Policy Type",
        "Policy Type",
        "Total Premium",
    )
    sns.barplot(x=summary.index, y=summary.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_monthly_claims(data):
    """Plot monthly claim counts using claim dates."""
    df = get_data(data, "claims")

    if "claim_date" not in df.columns:
        logger.warning("claim_date column is missing.")
        return None

    df["claim_date"] = pd.to_datetime(df["claim_date"], errors="coerce")
    df = df.dropna(subset=["claim_date"])

    if df.empty:
        return None

    df["month"] = df["claim_date"].dt.to_period("M").astype(str)
    summary = df.groupby("month").size()

    fig, ax = prepare_chart(
        "Monthly Claim Trend", "Month", "Number of Claims", (12, 5)
    )
    sns.lineplot(x=summary.index, y=summary.values, marker="o", ax=ax)
    return finish_chart(fig, ax, True)


def plot_claim_status(data):
    """Plot the distribution of claim statuses."""
    df = get_data(data, "claims")

    if "claim_status" not in df.columns:
        logger.warning("claim_status column is missing.")
        return None

    counts = df["claim_status"].fillna("Unknown").value_counts()

    fig, ax = prepare_chart(
        "Claim Status Distribution", "Claim Status", "Number of Claims"
    )
    sns.barplot(x=counts.index, y=counts.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_claim_type_distribution(data):
    """Plot the distribution of claim types."""
    df = get_data(data, "claims")

    if "claim_type" not in df.columns:
        logger.warning("claim_type column is missing.")
        return None

    counts = df["claim_type"].fillna("Unknown").value_counts()

    fig, ax = prepare_chart(
        "Claim Type Distribution", "Claim Type", "Number of Claims"
    )
    sns.barplot(x=counts.index, y=counts.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_claim_amount_distribution(data):
    """Plot the distribution of reported claim amounts."""
    df = get_data(data, "claims")
    amounts = numeric_column(df, "claim_amount").dropna()

    if amounts.empty:
        logger.warning("No valid claim amounts available.")
        return None

    fig, ax = prepare_chart(
        "Claim Amount Distribution", "Claim Amount", "Frequency"
    )
    sns.histplot(amounts, bins=30, kde=True, ax=ax)
    return finish_chart(fig, ax)


def plot_claim_amount_by_vehicle_type(data):
    """Plot average claim amount by vehicle type."""
    claims = get_data(data, "claims")
    vehicles = get_data(data, "vehicles")

    if "claim_amount" not in claims.columns:
        logger.warning("claim_amount column is missing.")
        return None

    # Use vehicle_type directly if it exists in claims.
    if "vehicle_type" not in claims.columns:
        if not {"vehicle_id", "vehicle_type"}.issubset(vehicles.columns):
            logger.warning("Vehicle type cannot be joined to claims.")
            return None

        if "vehicle_id" not in claims.columns:
            logger.warning("claims.vehicle_id column is missing.")
            return None

        vehicle_lookup = vehicles[
            ["vehicle_id", "vehicle_type"]
        ].drop_duplicates("vehicle_id")

        claims = claims.merge(
            vehicle_lookup,
            on="vehicle_id",
            how="left",
            validate="many_to_one",
        )

    claims["claim_amount"] = pd.to_numeric(
        claims["claim_amount"], errors="coerce"
    )
    summary = claims.groupby("vehicle_type")["claim_amount"].mean().dropna()

    if summary.empty:
        return None

    fig, ax = prepare_chart(
        "Average Claim Amount by Vehicle Type",
        "Vehicle Type",
        "Average Claim Amount",
    )
    sns.barplot(x=summary.index, y=summary.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_claims_by_region(data):
    """Plot the number of claims by region."""
    df = get_data(data, "claims")

    if "region" not in df.columns:
        logger.warning(
            "region column is missing from claims; "
            "join customer region if supported by the schema."
        )
        return None

    counts = df["region"].fillna("Unknown").value_counts()

    fig, ax = prepare_chart(
        "Claims by Region", "Region", "Number of Claims"
    )
    sns.barplot(x=counts.index, y=counts.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_claim_severity_by_region(data):
    """Plot average claim amount by region."""
    df = get_data(data, "claims")

    if not {"region", "claim_amount"}.issubset(df.columns):
        logger.warning("Region or claim amount column is missing.")
        return None

    df["claim_amount"] = pd.to_numeric(
        df["claim_amount"], errors="coerce"
    )
    summary = df.groupby("region")["claim_amount"].mean().dropna()

    if summary.empty:
        return None

    fig, ax = prepare_chart(
        "Average Claim Amount by Region",
        "Region",
        "Average Claim Amount",
    )
    sns.barplot(x=summary.index, y=summary.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_average_settlement_time(data):
    """Plot average settlement duration by claim status."""
    df = get_data(data, "claims")

    if "claim_settlement_days" in df.columns:
        df["settlement_days"] = pd.to_numeric(
            df["claim_settlement_days"], errors="coerce"
        )
    elif {"claim_date", "settlement_date"}.issubset(df.columns):
        df["claim_date"] = pd.to_datetime(
            df["claim_date"], errors="coerce"
        )
        df["settlement_date"] = pd.to_datetime(
            df["settlement_date"], errors="coerce"
        )
        df["settlement_days"] = (
            df["settlement_date"] - df["claim_date"]
        ).dt.days
    else:
        logger.warning("Settlement date columns are missing.")
        return None

    df = df[df["settlement_days"] >= 0]

    if "claim_status" in df.columns:
        summary = df.groupby("claim_status")["settlement_days"].mean()
        xlabel = "Claim Status"
    else:
        summary = pd.Series(
            {"All Claims": df["settlement_days"].mean()}
        )
        xlabel = "Claim Group"

    summary = summary.dropna()

    if summary.empty:
        return None

    fig, ax = prepare_chart(
        "Average Claim Settlement Time",
        xlabel,
        "Average Days",
    )
    sns.barplot(x=summary.index, y=summary.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_claim_to_premium_by_policy_type(data):
    """Plot claim amount divided by premium for each policy type."""
    policies = get_data(data, "policies")
    claims = get_data(data, "claims")

    required_policy = {"policy_id", "policy_type", "premium_amount"}
    required_claim = {"policy_id", "claim_amount"}

    if not required_policy.issubset(policies.columns):
        logger.warning("Required policy columns are missing.")
        return None

    if not required_claim.issubset(claims.columns):
        logger.warning("Required claim columns are missing.")
        return None

    policies["premium_amount"] = pd.to_numeric(
        policies["premium_amount"], errors="coerce"
    )
    claims["claim_amount"] = pd.to_numeric(
        claims["claim_amount"], errors="coerce"
    )

    premium_summary = policies.groupby("policy_type")["premium_amount"].sum()
    claims_with_type = claims.merge(
        policies[["policy_id", "policy_type"]].drop_duplicates("policy_id"),
        on="policy_id",
        how="left",
        validate="many_to_one",
    )
    claim_summary = claims_with_type.groupby("policy_type")[
        "claim_amount"
    ].sum()

    summary = pd.concat(
        [claim_summary.rename("claims"), premium_summary.rename("premium")],
        axis=1,
    ).fillna(0)

    summary = summary[summary["premium"] > 0]
    summary["ratio_percent"] = (
        summary["claims"] / summary["premium"] * 100
    )

    if summary.empty:
        return None

    fig, ax = prepare_chart(
        "Claim-to-Premium Ratio by Policy Type",
        "Policy Type",
        "Claim Amount / Premium (%)",
    )
    sns.barplot(x=summary.index, y=summary["ratio_percent"], ax=ax)
    return finish_chart(fig, ax, True)


def plot_vehicle_age_vs_claim_amount(data):
    """Plot vehicle age against claim amount."""
    claims = get_data(data, "claims")
    vehicles = get_data(data, "vehicles")

    if "claim_amount" not in claims.columns:
        return None

    if "vehicle_age" not in claims.columns:
        if not {"vehicle_id", "vehicle_age"}.issubset(vehicles.columns):
            logger.warning("Vehicle age is unavailable.")
            return None

        if "vehicle_id" not in claims.columns:
            return None

        claims = claims.merge(
            vehicles[["vehicle_id", "vehicle_age"]].drop_duplicates(
                "vehicle_id"
            ),
            on="vehicle_id",
            how="left",
            validate="many_to_one",
        )

    claims["claim_amount"] = pd.to_numeric(
        claims["claim_amount"], errors="coerce"
    )
    claims["vehicle_age"] = pd.to_numeric(
        claims["vehicle_age"], errors="coerce"
    )

    df = claims.dropna(subset=["vehicle_age", "claim_amount"])

    if df.empty:
        return None

    fig, ax = prepare_chart(
        "Vehicle Age vs Claim Amount",
        "Vehicle Age (Years)",
        "Claim Amount",
    )
    sns.scatterplot(
        data=df, x="vehicle_age", y="claim_amount", alpha=0.6, ax=ax
    )
    return finish_chart(fig, ax)


def plot_customer_age_vs_claim_amount(data):
    """Plot customer age against claim amount."""
    claims = get_data(data, "claims")
    customers = get_data(data, "customers")

    if "claim_amount" not in claims.columns:
        return None

    if "customer_age" not in claims.columns:
        if not {"customer_id", "customer_age"}.issubset(customers.columns):
            logger.warning("Customer age is unavailable.")
            return None

        if "customer_id" not in claims.columns:
            return None

        claims = claims.merge(
            customers[["customer_id", "customer_age"]].drop_duplicates(
                "customer_id"
            ),
            on="customer_id",
            how="left",
            validate="many_to_one",
        )

    claims["claim_amount"] = pd.to_numeric(
        claims["claim_amount"], errors="coerce"
    )
    claims["customer_age"] = pd.to_numeric(
        claims["customer_age"], errors="coerce"
    )

    df = claims.dropna(subset=["customer_age", "claim_amount"])

    if df.empty:
        return None

    fig, ax = prepare_chart(
        "Customer Age vs Claim Amount",
        "Customer Age (Years)",
        "Claim Amount",
    )
    sns.scatterplot(
        data=df, x="customer_age", y="claim_amount", alpha=0.6, ax=ax
    )
    return finish_chart(fig, ax)


def plot_vehicle_type_claim_performance(data):
    """Plot claim counts by vehicle type."""
    claims = get_data(data, "claims")
    vehicles = get_data(data, "vehicles")

    if "vehicle_type" not in claims.columns:
        if not {"vehicle_id", "vehicle_type"}.issubset(vehicles.columns):
            logger.warning("Vehicle type is unavailable.")
            return None

        if "vehicle_id" not in claims.columns:
            return None

        claims = claims.merge(
            vehicles[["vehicle_id", "vehicle_type"]].drop_duplicates(
                "vehicle_id"
            ),
            on="vehicle_id",
            how="left",
            validate="many_to_one",
        )

    counts = claims["vehicle_type"].fillna("Unknown").value_counts()

    fig, ax = prepare_chart(
        "Claim Counts by Vehicle Type",
        "Vehicle Type",
        "Number of Claims",
    )
    sns.barplot(x=counts.index, y=counts.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_damage_severity_distribution(data):
    """Plot the distribution of damage severity."""
    df = get_data(data, "claims")

    if "damage_severity" not in df.columns:
        logger.warning("damage_severity column is missing.")
        return None

    counts = df["damage_severity"].fillna("Unknown").value_counts()

    fig, ax = prepare_chart(
        "Damage Severity Distribution",
        "Damage Severity",
        "Number of Claims",
    )
    sns.barplot(x=counts.index, y=counts.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_payment_status(data):
    """Plot payment records by payment status."""
    df = get_data(data, "payments")

    if "payment_status" not in df.columns:
        logger.warning("payment_status column is missing.")
        return None

    counts = df["payment_status"].fillna("Unknown").value_counts()

    fig, ax = prepare_chart(
        "Payment Status Distribution",
        "Payment Status",
        "Number of Payments",
    )
    sns.barplot(x=counts.index, y=counts.values, ax=ax)
    return finish_chart(fig, ax, True)


def plot_monthly_premium_trend(data):
    """Plot total premium recorded by policy start month."""
    df = get_data(data, "policies")

    if not {"start_date", "premium_amount"}.issubset(df.columns):
        logger.warning("Policy start date or premium amount is missing.")
        return None

    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["premium_amount"] = pd.to_numeric(
        df["premium_amount"], errors="coerce"
    )
    df = df.dropna(subset=["start_date", "premium_amount"])

    if df.empty:
        return None

    df["month"] = df["start_date"].dt.to_period("M").astype(str)
    summary = df.groupby("month")["premium_amount"].sum()

    fig, ax = prepare_chart(
        "Monthly Premium Trend",
        "Month",
        "Total Premium",
        (12, 5),
    )
    sns.lineplot(x=summary.index, y=summary.values, marker="o", ax=ax)
    return finish_chart(fig, ax, True)


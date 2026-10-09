
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Motor Insurance Analytics",
    page_icon="🚗",
    layout="wide"
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"


# =========================================================
# 2. LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    """Load the five motor insurance CSV datasets."""
    data = {
        "customers": pd.read_csv(RAW_DATA_DIR / "customers.csv"),
        "policies": pd.read_csv(RAW_DATA_DIR / "policies.csv"),
        "vehicles": pd.read_csv(RAW_DATA_DIR / "vehicles.csv"),
        "claims": pd.read_csv(RAW_DATA_DIR / "claims.csv"),
        "payments": pd.read_csv(RAW_DATA_DIR / "payments.csv"),
    }

    for name, df in data.items():
        if df.empty:
            raise ValueError(f"{name}.csv contains no records.")

    # Convert date columns
    date_columns = {
        "customers": ["date_of_birth"],
        "policies": ["policy_start_date", "policy_end_date"],
        "claims": [
            "claim_date",
            "accident_date",
            "approval_date",
            "settlement_date",
        ],
        "payments": ["payment_date"],
    }

    for name, columns in date_columns.items():
        for column in columns:
            if column in data[name].columns:
                data[name][column] = pd.to_datetime(
                    data[name][column], errors="coerce"
                )

    # Convert numeric columns
    numeric_columns = {
        "policies": ["premium_amount", "coverage_amount"],
        "claims": ["claim_amount"],
        "payments": ["payment_amount"],
        "customers": ["age"],
        "vehicles": ["vehicle_value", "vehicle_year"],
    }

    for name, columns in numeric_columns.items():
        for column in columns:
            if column in data[name].columns:
                data[name][column] = pd.to_numeric(
                    data[name][column], errors="coerce"
                )

    return data


# =========================================================
# 3. VALIDATE AND PREPARE DATA
# =========================================================

try:
    data = load_data()

    customers = data["customers"]
    policies = data["policies"]
    vehicles = data["vehicles"]
    claims = data["claims"]
    payments = data["payments"]

    required_columns = {
        "customers": {"customer_id"},
        "policies": {
            "policy_id", "customer_id", "vehicle_id",
            "premium_amount", "policy_status", "policy_type"
        },
        "vehicles": {"vehicle_id", "vehicle_type"},
        "claims": {
            "claim_id", "policy_id", "claim_amount", "claim_status"
        },
        "payments": {"payment_id", "payment_amount", "payment_status"},
    }

    for name, required in required_columns.items():
        missing = required - set(data[name].columns)
        if missing:
            st.error(
                f"{name}.csv is missing required columns: "
                f"{', '.join(sorted(missing))}"
            )
            st.stop()

    # Avoid multiplying policy rows when joining related tables.
    # Duplicate IDs are reported rather than silently deduplicated.
    for name, df, key in [
        ("customers", customers, "customer_id"),
        ("policies", policies, "policy_id"),
        ("vehicles", vehicles, "vehicle_id"),
        ("claims", claims, "claim_id"),
        ("payments", payments, "payment_id"),
    ]:
        if df[key].isna().any():
            st.error(f"{name}.csv contains missing {key} values.")
            st.stop()

        if df[key].duplicated().any():
            st.error(
                f"{name}.csv contains duplicate {key} values. "
                "Please check the source data before calculating KPIs."
            )
            st.stop()

    # Build policy-level view: one row per policy.
    customer_columns = [
        c for c in [
            "customer_id", "age", "gender", "city",
            "state", "occupation"
        ] if c in customers.columns
    ]

    vehicle_columns = [
        c for c in [
            "vehicle_id", "vehicle_type", "vehicle_make",
            "vehicle_model", "vehicle_value", "vehicle_year"
        ] if c in vehicles.columns
    ]

    policy_view = policies.merge(
        customers[customer_columns],
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    policy_view = policy_view.merge(
        vehicles[vehicle_columns],
        on="vehicle_id",
        how="left",
        validate="many_to_one"
    )

    # Region is derived from customer state, falling back to city.
    policy_view["region"] = (
        policy_view.get("state", pd.Series(index=policy_view.index))
        .fillna(policy_view.get("city", pd.Series(index=policy_view.index)))
        .fillna("Unknown")
    )

    # Build claim-level view: one row per claim.
    claim_policy_columns = [
        c for c in [
            "policy_id", "policy_type", "premium_amount",
            "policy_status", "customer_id", "age", "region",
            "vehicle_id", "vehicle_type"
        ] if c in policy_view.columns
    ]

    claim_view = claims.merge(
        policy_view[claim_policy_columns],
        on="policy_id",
        how="left",
        validate="many_to_one",
        suffixes=("", "_policy")
    )

    # Settlement duration measured from claim registration to settlement.
    claim_view["settlement_days"] = (
        claim_view["settlement_date"] - claim_view["claim_date"]
    ).dt.total_seconds() / 86400

    claim_view.loc[
        claim_view["settlement_days"] < 0, "settlement_days"
    ] = float("nan")

except FileNotFoundError as error:
    st.error(f"Could not find a dataset file: {error}")
    st.info("Check that all five CSV files are inside data/raw/.")
    st.stop()

except Exception as error:
    st.error(f"Unable to load or prepare data: {error}")
    st.stop()


# =========================================================
# 4. DASHBOARD HEADER
# =========================================================

st.title("🚗 Motor Insurance Analytics Dashboard")
st.caption(
    "Policy performance | Claims analysis | Customer insights | Payments"
)

st.success("All five datasets loaded from data/raw/.")


# =========================================================
# 5. SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Dashboard Filters")

def filter_options(df, column):
    """Return sorted, non-empty filter values."""
    if column not in df.columns:
        return []
    return sorted(
        df[column].dropna().astype(str).unique().tolist()
    )


def multi_filter(label, options):
    """Display a multiselect with all values selected by default."""
    return st.sidebar.multiselect(
        label,
        options,
        default=options
    )


policy_statuses = filter_options(policy_view, "policy_status")
policy_types = filter_options(policy_view, "policy_type")
vehicle_types = filter_options(policy_view, "vehicle_type")
regions = filter_options(policy_view, "region")

selected_statuses = multi_filter("Policy Status", policy_statuses)
selected_types = multi_filter("Policy Type", policy_types)
selected_vehicles = multi_filter("Vehicle Type", vehicle_types)
selected_regions = multi_filter("Region", regions)

filtered_policies = policy_view[
    policy_view["policy_status"].astype(str).isin(selected_statuses)
    & policy_view["policy_type"].astype(str).isin(selected_types)
    & policy_view["vehicle_type"].astype(str).isin(selected_vehicles)
    & policy_view["region"].astype(str).isin(selected_regions)
].copy()

selected_policy_ids = filtered_policies["policy_id"]

filtered_claims = claim_view[
    claim_view["policy_id"].isin(selected_policy_ids)
].copy()

# Keep payments as a separate fact table. Do not join payment rows
# directly to policies or claims for financial KPI calculations.
filtered_payments = payments[
    payments["policy_id"].isin(selected_policy_ids)
].copy() if "policy_id" in payments.columns else payments.iloc[0:0].copy()


# =========================================================
# 6. KPI CARDS
# =========================================================

total_policies = filtered_policies["policy_id"].nunique()
total_premium = filtered_policies["premium_amount"].sum()

total_claims = filtered_claims["claim_id"].nunique()
total_claim_amount = filtered_claims["claim_amount"].sum()

approved_mask = (
    filtered_claims["claim_status"]
    .astype(str).str.strip().str.lower().eq("approved")
)

approved_claim_amount = filtered_claims.loc[
    approved_mask, "claim_amount"
].sum()

claim_to_premium = (
    total_claim_amount / total_premium * 100
    if total_premium and pd.notna(total_premium)
    else 0
)

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Policies", f"{total_policies:,}")
k2.metric("Total Premium", f"₹{total_premium:,.0f}")
k3.metric("Total Claims", f"{total_claims:,}")
k4.metric("Recorded Claim Amount", f"₹{total_claim_amount:,.0f}")

k5, k6, k7, k8 = st.columns(4)

k5.metric(
    "Approved Claims",
    f"{filtered_claims.loc[approved_mask, 'claim_id'].nunique():,}"
)
k6.metric("Approved Claim Amount", f"₹{approved_claim_amount:,.0f}")
k7.metric("Claim Amount / Premium", f"{claim_to_premium:.2f}%")
k8.metric("Payment Records", f"{filtered_payments['payment_id'].nunique():,}")

st.caption(
    "Claim Amount / Premium is an indicative comparison of recorded claim "
    "amounts against policy premium amounts, not an actuarial loss ratio. "
    "The premium total reflects policy premium records, not necessarily "
    "earned premium."
)


# =========================================================
# 7. POLICY ANALYSIS
# =========================================================

st.header("1. Policy Analysis")

c1, c2 = st.columns(2)

with c1:
    status_counts = (
        filtered_policies.groupby("policy_status", dropna=False)
        ["policy_id"].nunique()
        .reset_index(name="policy_count")
    )

    if not status_counts.empty:
        fig = px.pie(
            status_counts,
            names="policy_status",
            values="policy_count",
            title="Policies by Status",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

with c2:
    premium_type = (
        filtered_policies.groupby("policy_type", dropna=False)
        ["premium_amount"].sum()
        .reset_index()
        .sort_values("premium_amount", ascending=False)
    )

    if not premium_type.empty:
        fig = px.bar(
            premium_type,
            x="policy_type",
            y="premium_amount",
            title="Total Premium by Policy Type",
            labels={
                "policy_type": "Policy Type",
                "premium_amount": "Premium Amount (₹)"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Policy Summary")
st.dataframe(
    filtered_policies[
        ["policy_id", "policy_status", "policy_type", "premium_amount",
         "vehicle_type", "region"]
    ],
    use_container_width=True,
    hide_index=True
)


# =========================================================
# 8. CLAIMS ANALYSIS
# =========================================================

st.header("2. Claims Analysis")

c1, c2 = st.columns(2)

with c1:
    claim_status_counts = (
        filtered_claims.groupby("claim_status", dropna=False)
        ["claim_id"].nunique()
        .reset_index(name="claim_count")
    )

    if not claim_status_counts.empty:
        fig = px.bar(
            claim_status_counts,
            x="claim_status",
            y="claim_count",
            title="Claims by Status",
            labels={
                "claim_status": "Claim Status",
                "claim_count": "Number of Claims"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

with c2:
    claim_type_amount = (
        filtered_claims.groupby("claim_type", dropna=False)
        ["claim_amount"].sum()
        .reset_index()
        .sort_values("claim_amount", ascending=False)
    ) if "claim_type" in filtered_claims.columns else pd.DataFrame()

    if not claim_type_amount.empty:
        fig = px.bar(
            claim_type_amount,
            x="claim_type",
            y="claim_amount",
            title="Claim Amount by Claim Type",
            labels={
                "claim_type": "Claim Type",
                "claim_amount": "Claim Amount (₹)"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    vehicle_claims = (
        filtered_claims.groupby("vehicle_type", dropna=False)
        ["claim_id"].nunique()
        .reset_index(name="claim_count")
        .sort_values("claim_count", ascending=False)
    )

    if not vehicle_claims.empty:
        fig = px.bar(
            vehicle_claims,
            x="vehicle_type",
            y="claim_count",
            title="Number of Claims by Vehicle Type"
        )
        st.plotly_chart(fig, use_container_width=True)

with c2:
    region_claims = (
        filtered_claims.groupby("region", dropna=False)
        ["claim_amount"].sum()
        .reset_index()
        .sort_values("claim_amount", ascending=False)
    )

    if not region_claims.empty:
        fig = px.bar(
            region_claims,
            x="region",
            y="claim_amount",
            title="Recorded Claim Amount by Region",
            labels={"claim_amount": "Claim Amount (₹)"}
        )
        st.plotly_chart(fig, use_container_width=True)

# Settlement time
settlement_data = filtered_claims.dropna(subset=["settlement_days"])

settlement_data = settlement_data[
    settlement_data["settlement_days"] >= 0
]

if not settlement_data.empty:
    st.subheader("Claim Settlement Time")

    average_days = settlement_data["settlement_days"].mean()
    st.metric(
        "Average Claim Registration-to-Settlement Time",
        f"{average_days:.1f} days"
    )

    fig = px.histogram(
        settlement_data,
        x="settlement_days",
        nbins=20,
        title="Distribution of Claim Settlement Time",
        labels={"settlement_days": "Days to Settlement"}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info(
        "No valid claim registration and settlement date pairs "
        "are available for this filter selection."
    )


# =========================================================
# 9. CUSTOMER ANALYSIS
# =========================================================

st.header("3. Customer Analysis")

age_data = filtered_claims.dropna(subset=["age"]).copy()

if not age_data.empty:
    age_data["age_group"] = pd.cut(
        age_data["age"],
        bins=[0, 25, 35, 45, 60, 120],
        labels=["18–25", "26–35", "36–45", "46–60", "60+"],
        include_lowest=True
    )

    age_summary = (
        age_data.groupby("age_group", observed=False)
        ["claim_amount"].sum()
        .reset_index()
    )

    fig = px.bar(
        age_summary,
        x="age_group",
        y="claim_amount",
        title="Recorded Claim Amount by Customer Age Group",
        labels={
            "age_group": "Age Group",
            "claim_amount": "Claim Amount (₹)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "This compares total recorded claim amounts, not the risk rate "
        "per customer. Segment sizes should be considered."
    )
else:
    st.info("Customer age is not available for the selected claims.")


# =========================================================
# 10. PAYMENT ANALYSIS
# =========================================================

st.header("4. Payment Analysis")

c1, c2 = st.columns(2)

with c1:
    payment_status_summary = (
        filtered_payments.groupby("payment_status", dropna=False)
        ["payment_id"].nunique()
        .reset_index(name="payment_count")
    )

    if not payment_status_summary.empty:
        fig = px.bar(
            payment_status_summary,
            x="payment_status",
            y="payment_count",
            title="Payment Records by Status"
        )
        st.plotly_chart(fig, use_container_width=True)

with c2:
    payment_method_summary = (
        filtered_payments.groupby("payment_method", dropna=False)
        ["payment_amount"].sum()
        .reset_index()
        .sort_values("payment_amount", ascending=False)
    ) if "payment_method" in filtered_payments.columns else pd.DataFrame()

    if not payment_method_summary.empty:
        fig = px.bar(
            payment_method_summary,
            x="payment_method",
            y="payment_amount",
            title="Payment Amount by Payment Method",
            labels={"payment_amount": "Payment Amount (₹)"}
        )
        st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Payments are reported separately because the schema does not identify "
    "whether each payment is a premium installment or a claim settlement."
)


# =========================================================
# 11. BUSINESS ATTENTION
# =========================================================

st.header("5. Business Attention")

attention = []

if not filtered_claims.empty:
    # Claim statuses requiring review; unknown status names remain visible
    # in the full claims-by-status chart above.
    pending_mask = filtered_claims["claim_status"].astype(str).str.lower().str.contains(
        "pending|review|processing", na=False
    )
    rejected_mask = filtered_claims["claim_status"].astype(str).str.lower().str.contains(
        "reject|denied", na=False
    )

    pending_count = filtered_claims.loc[pending_mask, "claim_id"].nunique()
    rejected_count = filtered_claims.loc[rejected_mask, "claim_id"].nunique()

    if pending_count:
        attention.append(
            f"{pending_count:,} claims have a pending, review, or processing status."
        )

    if rejected_count:
        attention.append(
            f"{rejected_count:,} claims have a rejected or denied status; "
            "review rejection reasons before drawing conclusions."
        )

if not settlement_data.empty:
    long_settlements = settlement_data[
        settlement_data["settlement_days"] > 30
    ]["claim_id"].nunique()

    if long_settlements:
        attention.append(
            f"{long_settlements:,} claims took more than 30 days "
            "from registration to settlement."
        )

if not region_claims.empty:
    highest_region = region_claims.iloc[0]
    attention.append(
        f"Region with the highest recorded claim amount: "
        f"{highest_region['region']} "
        f"(₹{highest_region['claim_amount']:,.0f})."
    )

if attention:
    for item in attention:
        st.warning(item)
else:
    st.info(
        "No attention items were identified for these filters. "
        "Check the charts and status definitions for further investigation."
    )

st.caption(
    "These are descriptive indicators, not proof of fraud or poor performance. "
    "Investigate claim volume, exposure, severity, and operational context."
)


# =========================================================
# 12. DATA EXPLORER AND DOWNLOAD
# =========================================================

st.header("6. Data Explorer")

dataset_choice = st.selectbox(
    "Choose a dataset",
    ["Policies", "Claims", "Customers", "Vehicles", "Payments"]
)

dataset_map = {
    "Policies": filtered_policies,
    "Claims": filtered_claims,
    "Customers": customers,
    "Vehicles": vehicles,
    "Payments": filtered_payments,
}

selected_data = dataset_map[dataset_choice]

st.dataframe(
    selected_data,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label=f"Download {dataset_choice} CSV",
    data=selected_data.to_csv(index=False).encode("utf-8"),
    file_name=f"{dataset_choice.lower()}_filtered.csv",
    mime="text/csv"
)

st.caption("Motor Insurance Analytics | Data loaded from local project files.")


"""
Validate motor insurance datasets.

Checks required columns, primary keys, and relationships
between customers, policies, vehicles, claims, and payments.
"""

import pandas as pd


REQUIRED_COLUMNS = {
    "customers": ["customer_id"],
    "policies": ["policy_id", "customer_id", "vehicle_id"],
    "vehicles": ["vehicle_id"],
    "claims": ["claim_id", "policy_id", "customer_id"],
    "payments": ["payment_id", "claim_id", "policy_id"],
}


def validate_customers(df):
    """Validate customer data and customer IDs."""
    return validate_table(df, "customers")


def validate_vehicles(df):
    """Validate vehicle data and vehicle IDs."""
    return validate_table(df, "vehicles")


def validate_policies(df):
    """Validate policy data and policy IDs."""
    return validate_table(df, "policies")


def validate_claims(df):
    """Validate claim data and claim IDs."""
    return validate_table(df, "claims")


def validate_payments(df):
    """Validate payment data and payment IDs."""
    return validate_table(df, "payments")


def validate_table(df, table_name):
    """Check required columns, missing IDs, and duplicate IDs."""
    errors = []

    if table_name not in REQUIRED_COLUMNS:
        return [f"Unknown table: {table_name}"]

    required = REQUIRED_COLUMNS[table_name]
    missing_columns = [
        column for column in required if column not in df.columns
    ]

    if missing_columns:
        return [
            f"{table_name}: missing required columns {missing_columns}"
        ]

    id_column = required[0]

    if df[id_column].isna().any():
        errors.append(f"{table_name}: {id_column} contains missing values")

    if df[id_column].duplicated().any():
        errors.append(f"{table_name}: duplicate {id_column} values found")

    return errors


def validate_relationships(data):
    """Check foreign keys across the five insurance datasets."""
    errors = []

    relationships = [
        ("policies", "customer_id", "customers", "customer_id"),
        ("policies", "vehicle_id", "vehicles", "vehicle_id"),
        ("claims", "policy_id", "policies", "policy_id"),
        ("claims", "customer_id", "customers", "customer_id"),
        ("payments", "claim_id", "claims", "claim_id"),
        ("payments", "policy_id", "policies", "policy_id"),
    ]

    for child_name, child_key, parent_name, parent_key in relationships:
        child = data[child_name]
        parent = data[parent_name]

        if child_key not in child.columns:
            errors.append(
                f"{child_name}: missing foreign-key column {child_key}"
            )
            continue

        if parent_key not in parent.columns:
            errors.append(
                f"{parent_name}: missing referenced column {parent_key}"
            )
            continue

        # Ignore missing foreign keys here; report them separately.
        foreign_keys = child[child_key].dropna()
        unmatched = ~foreign_keys.isin(parent[parent_key])

        if unmatched.any():
            errors.append(
                f"{child_name}.{child_key}: "
                f"{int(unmatched.sum())} values have no matching "
                f"{parent_name}.{parent_key}"
            )

        missing_fk_count = int(child[child_key].isna().sum())
        if missing_fk_count:
            errors.append(
                f"{child_name}.{child_key}: "
                f"{missing_fk_count} missing foreign-key values"
            )

    return errors


def validate_all_tables(data):
    """Run table-level and relationship validation."""
    validators = {
        "customers": validate_customers,
        "vehicles": validate_vehicles,
        "policies": validate_policies,
        "claims": validate_claims,
        "payments": validate_payments,
    }

    errors = []

    for table_name, validator in validators.items():
        if table_name not in data:
            errors.append(f"Missing dataset: {table_name}")
            continue

        errors.extend(validator(data[table_name]))

    required_tables = set(REQUIRED_COLUMNS)
    if required_tables.issubset(data.keys()):
        errors.extend(validate_relationships(data))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
    else:
        print("All table and relationship validations passed.")

    return errors


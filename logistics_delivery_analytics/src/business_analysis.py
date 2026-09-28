import pandas as pd


def calculate_total_orders(df):
    """Calculate the total number of orders."""
    return df["order_id"].nunique()


def calculate_total_delivered(df):
    """Calculate the total number of delivered orders."""
    if "delivery_status" in df.columns:
        return (df["delivery_status"].str.lower() == "delivered").sum()

    return 0


def calculate_total_delayed(df):
    """Calculate the total number of delayed orders."""
    return (df["delay_days"] > 0).sum()


def calculate_on_time_percentage(df):
    """Calculate the percentage of orders delivered on time."""
    if len(df) == 0:
        return 0

    return df["on_time_flag"].mean() * 100


def calculate_average_delivery_days(df):
    """Calculate the average delivery time in days."""
    return df["delivery_days"].mean()


def calculate_average_delay_days(df):
    """Calculate the average delay in days."""
    delayed = df[df["delay_days"] > 0]

    if delayed.empty:
        return 0

    return delayed["delay_days"].mean()


def calculate_total_shipping_cost(df):
    """Calculate total shipping cost."""
    return df["shipping_cost"].sum()


def calculate_average_shipping_cost(df):
    """Calculate average shipping cost."""
    return df["shipping_cost"].mean()


def calculate_total_fuel_cost(df):
    """Calculate total fuel cost."""
    return df["fuel_cost"].sum()


def calculate_total_logistics_cost(df):
    """Calculate total logistics cost."""
    return df["total_logistics_cost"].sum()


def calculate_average_logistics_cost(df):
    """Calculate average logistics cost."""
    return df["total_logistics_cost"].mean()


def calculate_average_cost_per_km(df):
    """Calculate average cost per kilometer."""
    return df["cost_per_km"].mean()


def analyze_route_performance(df):
    """Analyze delivery performance by route."""
    result = df.groupby(
        ["origin_city", "destination_city"]
    ).agg(
        total_orders=("order_id", "count"),
        on_time_percentage=("on_time_flag", "mean"),
        average_delivery_days=("delivery_days", "mean")
    ).reset_index()

    result["on_time_percentage"] *= 100

    return result


def analyze_route_cost(df):
    """Analyze logistics cost by route."""
    return df.groupby(
        ["origin_city", "destination_city"]
    ).agg(
        total_orders=("order_id", "count"),
        total_logistics_cost=("total_logistics_cost", "sum"),
        average_logistics_cost=("total_logistics_cost", "mean"),
        average_cost_per_km=("cost_per_km", "mean")
    ).reset_index()


def analyze_route_delays(df):
    """Analyze delivery delays by route."""
    return df.groupby(
        ["origin_city", "destination_city"]
    ).agg(
        total_orders=("order_id", "count"),
        average_delay_days=("delay_days", "mean"),
        delayed_orders=("delay_days", lambda x: (x > 0).sum())
    ).reset_index()


def analyze_warehouse_performance(df):
    """Analyze delivery performance by warehouse."""
    result = df.groupby("warehouse").agg(
        total_orders=("order_id", "count"),
        on_time_percentage=("on_time_flag", "mean"),
        average_delivery_days=("delivery_days", "mean")
    ).reset_index()

    result["on_time_percentage"] *= 100

    return result


def analyze_warehouse_delays(df):
    """Analyze delays by warehouse."""
    return df.groupby("warehouse").agg(
        total_orders=("order_id", "count"),
        average_delay_days=("delay_days", "mean"),
        delayed_orders=("delay_days", lambda x: (x > 0).sum())
    ).reset_index()


def analyze_warehouse_processing_time(df):
    """Analyze warehouse processing time."""
    return df.groupby("warehouse").agg(
        average_processing_hours=(
            "warehouse_processing_hours",
            "mean"
        ),
        total_orders=("order_id", "count")
    ).reset_index()


def analyze_shipping_mode(df):
    """Analyze performance by shipping mode."""
    result = df.groupby("shipping_mode").agg(
        total_orders=("order_id", "count"),
        on_time_percentage=("on_time_flag", "mean"),
        average_delivery_days=("delivery_days", "mean")
    ).reset_index()

    result["on_time_percentage"] *= 100

    return result


def analyze_shipping_mode_cost(df):
    """Analyze cost by shipping mode."""
    return df.groupby("shipping_mode").agg(
        total_orders=("order_id", "count"),
        total_logistics_cost=("total_logistics_cost", "sum"),
        average_logistics_cost=("total_logistics_cost", "mean")
    ).reset_index()


def analyze_shipping_mode_delays(df):
    """Analyze delays by shipping mode."""
    return df.groupby("shipping_mode").agg(
        total_orders=("order_id", "count"),
        average_delay_days=("delay_days", "mean"),
        delayed_orders=("delay_days", lambda x: (x > 0).sum())
    ).reset_index()


def analyze_delivery_partner(df):
    """Analyze delivery partner performance."""
    result = df.groupby("delivery_partner").agg(
        total_orders=("order_id", "count"),
        on_time_percentage=("on_time_flag", "mean"),
        average_delivery_days=("delivery_days", "mean")
    ).reset_index()

    result["on_time_percentage"] *= 100

    return result


def analyze_partner_cost(df):
    """Analyze logistics cost by delivery partner."""
    return df.groupby("delivery_partner").agg(
        total_orders=("order_id", "count"),
        total_logistics_cost=("total_logistics_cost", "sum"),
        average_logistics_cost=("total_logistics_cost", "mean")
    ).reset_index()


def analyze_partner_delays(df):
    """Analyze delays by delivery partner."""
    return df.groupby("delivery_partner").agg(
        total_orders=("order_id", "count"),
        average_delay_days=("delay_days", "mean"),
        delayed_orders=("delay_days", lambda x: (x > 0).sum())
    ).reset_index()


def analyze_partner_damage_rate(df):
    """Calculate damage rate by delivery partner."""
    result = df.groupby("delivery_partner").agg(
        total_orders=("order_id", "count"),
        damaged_orders=("damage_flag", "sum")
    ).reset_index()

    result["damage_rate"] = (
        result["damaged_orders"]
        / result["total_orders"]
        * 100
    )

    return result


def calculate_average_customer_rating(df):
    """Calculate average customer rating."""
    return df["customer_rating"].mean()


def calculate_return_rate(df):
    """Calculate the percentage of returned orders."""
    if len(df) == 0:
        return 0

    return df["return_flag"].mean() * 100


def calculate_damage_rate(df):
    """Calculate the percentage of damaged orders."""
    if len(df) == 0:
        return 0

    return df["damage_flag"].mean() * 100
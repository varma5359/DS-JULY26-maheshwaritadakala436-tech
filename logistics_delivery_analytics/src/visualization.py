import matplotlib.pyplot as plt
import seaborn as sns


def plot_delivery_status(df):
    """Plot the number of orders by delivery status."""

    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=df,
        x="delivery_status"
    )

    plt.title("Delivery Status Distribution")
    plt.xlabel("Delivery Status")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.show()


def plot_monthly_orders(df):
    """Plot monthly order volume."""

    data = df.copy()

    data["month"] = (
        data["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_orders = (
        data.groupby("month")
        .size()
    )

    plt.figure(figsize=(10, 5))

    monthly_orders.plot(
        kind="line",
        marker="o"
    )

    plt.title("Monthly Orders")
    plt.xlabel("Month")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_monthly_delivery_performance(df):
    """Plot monthly on-time delivery percentage."""

    data = df.copy()

    data["month"] = (
        data["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_performance = (
        data.groupby("month")["on_time_flag"]
        .mean()
        * 100
    )

    plt.figure(figsize=(10, 5))

    monthly_performance.plot(
        kind="line",
        marker="o"
    )

    plt.title("Monthly On-Time Delivery Performance")
    plt.xlabel("Month")
    plt.ylabel("On-Time Delivery (%)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_delay_by_warehouse(df):
    """Plot average delivery delay by warehouse."""

    data = (
        df.groupby("warehouse")["delay_days"]
        .mean()
        .sort_values()
    )

    plt.figure(figsize=(8, 5))

    data.plot(kind="bar")

    plt.title("Average Delay by Warehouse")
    plt.xlabel("Warehouse")
    plt.ylabel("Average Delay (Days)")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_delay_by_shipping_mode(df):
    """Plot average delivery delay by shipping mode."""

    data = (
        df.groupby("shipping_mode")["delay_days"]
        .mean()
        .sort_values()
    )

    plt.figure(figsize=(8, 5))

    data.plot(kind="bar")

    plt.title("Average Delay by Shipping Mode")
    plt.xlabel("Shipping Mode")
    plt.ylabel("Average Delay (Days)")

    plt.tight_layout()
    plt.show()


def plot_delay_by_route(df):
    """Plot average delivery delay by route."""

    data = (
        df.groupby(
            ["origin_city", "destination_city"]
        )["delay_days"]
        .mean()
        .sort_values()
    )

    labels = [
        f"{origin} → {destination}"
        for origin, destination in data.index
    ]

    plt.figure(figsize=(10, 7))

    plt.barh(
        labels,
        data.values
    )

    plt.title("Average Delay by Route")
    plt.xlabel("Average Delay (Days)")
    plt.ylabel("Route")

    plt.tight_layout()
    plt.show()


def plot_delay_distribution(df):
    """Plot the distribution of delivery delays."""

    plt.figure(figsize=(9, 5))

    sns.histplot(
        data=df,
        x="delay_days",
        bins=20,
        kde=True
    )

    plt.axvline(
        0,
        linestyle="--"
    )

    plt.title("Delivery Delay Distribution")
    plt.xlabel("Delay (Days)")
    plt.ylabel("Number of Orders")

    plt.tight_layout()
    plt.show()


def plot_cost_by_shipping_mode(df):
    """Plot average logistics cost by shipping mode."""

    data = (
        df.groupby("shipping_mode")[
            "total_logistics_cost"
        ]
        .mean()
        .sort_values()
    )

    plt.figure(figsize=(8, 5))

    data.plot(kind="bar")

    plt.title("Average Logistics Cost by Shipping Mode")
    plt.xlabel("Shipping Mode")
    plt.ylabel("Average Logistics Cost")

    plt.tight_layout()
    plt.show()


def plot_cost_by_route(df):
    """Plot average logistics cost by route."""

    data = (
        df.groupby(
            ["origin_city", "destination_city"]
        )["total_logistics_cost"]
        .mean()
        .sort_values()
    )

    labels = [
        f"{origin} → {destination}"
        for origin, destination in data.index
    ]

    plt.figure(figsize=(10, 7))

    plt.barh(
        labels,
        data.values
    )

    plt.title("Average Logistics Cost by Route")
    plt.xlabel("Average Logistics Cost")
    plt.ylabel("Route")

    plt.tight_layout()
    plt.show()


def plot_cost_trend(df):
    """Plot monthly logistics cost trend."""

    data = df.copy()

    data["month"] = (
        data["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_cost = (
        data.groupby("month")[
            "total_logistics_cost"
        ]
        .sum()
    )

    plt.figure(figsize=(10, 5))

    monthly_cost.plot(
        kind="line",
        marker="o"
    )

    plt.title("Monthly Logistics Cost Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Logistics Cost")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_orders_by_warehouse(df):
    """Plot number of orders handled by warehouse."""

    data = (
        df["warehouse"]
        .value_counts()
    )

    plt.figure(figsize=(8, 5))

    data.plot(kind="bar")

    plt.title("Orders by Warehouse")
    plt.xlabel("Warehouse")
    plt.ylabel("Number of Orders")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_processing_time_by_warehouse(df):
    """Plot average warehouse processing time."""

    data = (
        df.groupby("warehouse")[
            "warehouse_processing_hours"
        ]
        .mean()
        .sort_values()
    )

    plt.figure(figsize=(8, 5))

    data.plot(kind="bar")

    plt.title("Average Processing Time by Warehouse")
    plt.xlabel("Warehouse")
    plt.ylabel("Processing Time (Hours)")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_shipments_by_partner(df):
    """Plot number of shipments handled by each partner."""

    data = (
        df["delivery_partner"]
        .value_counts()
    )

    plt.figure(figsize=(8, 5))

    data.plot(kind="bar")

    plt.title("Shipments by Delivery Partner")
    plt.xlabel("Delivery Partner")
    plt.ylabel("Number of Shipments")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_partner_delivery_performance(df):
    """Plot on-time delivery percentage by partner."""

    data = (
        df.groupby("delivery_partner")[
            "on_time_flag"
        ]
        .mean()
        * 100
    )

    data = data.sort_values()

    plt.figure(figsize=(8, 5))

    data.plot(kind="bar")

    plt.title("Partner Delivery Performance")
    plt.xlabel("Delivery Partner")
    plt.ylabel("On-Time Delivery (%)")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_partner_cost(df):
    """Plot average logistics cost by delivery partner."""

    data = (
        df.groupby("delivery_partner")[
            "total_logistics_cost"
        ]
        .mean()
        .sort_values()
    )

    plt.figure(figsize=(8, 5))

    data.plot(kind="bar")

    plt.title("Average Logistics Cost by Partner")
    plt.xlabel("Delivery Partner")
    plt.ylabel("Average Logistics Cost")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_customer_rating_distribution(df):
    """Plot customer rating distribution."""

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x="customer_rating",
        bins=5,
        discrete=True
    )

    plt.title("Customer Rating Distribution")
    plt.xlabel("Customer Rating")
    plt.ylabel("Number of Orders")

    plt.tight_layout()
    plt.show()


def plot_rating_by_delivery_status(df):
    """Plot average customer rating by delivery status."""

    data = (
        df.groupby("delivery_status")[
            "customer_rating"
        ]
        .mean()
    )

    plt.figure(figsize=(8, 5))

    data.plot(kind="bar")

    plt.title("Average Customer Rating by Delivery Status")
    plt.xlabel("Delivery Status")
    plt.ylabel("Average Customer Rating")

    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.show()
from src.data_loader import load_data
from src.data_cleaner import clean_data, save_cleaned_data


def run_pipeline():
    """Run the complete logistics data processing pipeline."""

    input_path = "data/raw/logistics_data.csv"
    output_path = "data/cleaned/logistics_cleaned.csv"

    print("=" * 50)
    print("LOGISTICS DELIVERY ANALYTICS")
    print("=" * 50)

    print("\n1. Loading raw data...")

    df = load_data(input_path)

    print("Data loaded successfully!")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\n2. Cleaning data...")

    cleaned_df = clean_data(df)

    print("Data cleaning completed!")
    print(f"Cleaned rows: {cleaned_df.shape[0]}")
    print(f"Cleaned columns: {cleaned_df.shape[1]}")

    print("\n3. Saving cleaned data...")

    save_cleaned_data(
        cleaned_df,
        output_path
    )

    print(
        f"Cleaned data saved to: {output_path}"
    )

    print("\n4. Derived columns created:")

    derived_columns = [
        "delivery_days",
        "delay_days",
        "cost_per_km",
        "total_logistics_cost",
        "on_time_flag"
    ]

    for column in derived_columns:
        print(f"   - {column}")

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
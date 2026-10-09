
"""
Main execution file for the Motor Insurance Analytics project.

Workflow:
1. Load raw datasets.
2. Clean and transform data.
3. Validate datasets and relationships.
4. Calculate business KPIs.
5. Generate business insights.
6. Create and save visualizations.
7. Save cleaned datasets and log execution.
"""

from pathlib import Path

from src.data_loader import load_all_data
from src.data_cleaner import clean_data, save_cleaned_data
from src.validation import validate_all_tables
from src.insurance_analysis import analyze_business
from src.insights import (
    generate_portfolio_insights,
    generate_claim_insights,
    generate_premium_insights,
    generate_customer_insights,
    generate_vehicle_insights,
    generate_risk_patterns,
    generate_business_recommendations,
)
from src.visualization import (
    plot_policy_status,
    plot_policy_type_distribution,
    plot_premium_by_policy_type,
    plot_monthly_claims,
    plot_claim_status,
    plot_claim_type_distribution,
    plot_claim_amount_distribution,
    plot_claim_amount_by_vehicle_type,
    plot_claims_by_region,
    plot_claim_severity_by_region,
    plot_average_settlement_time,
    plot_claim_to_premium_by_policy_type,
    plot_vehicle_age_vs_claim_amount,
    plot_customer_age_vs_claim_amount,
    plot_vehicle_type_claim_performance,
    plot_damage_severity_distribution,
    plot_payment_status,
    plot_monthly_premium_trend,
)
from src.logger import setup_logger, log_pipeline_step, log_exception


# Project directories
BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
CLEANED_DATA_DIR = BASE_DIR / "data" / "cleaned"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"


def run_pipeline():
    """Execute the complete motor insurance analytics workflow."""
    logger = setup_logger(LOGS_DIR)

    try:
        # Step 1: Load datasets
        log_pipeline_step(logger, "Loading raw datasets")

        data = load_all_data(RAW_DATA_DIR)

        logger.info("Loaded datasets: %s", list(data.keys()))

        # Step 2: Clean datasets
        log_pipeline_step(logger, "Cleaning datasets")

        cleaned_data = clean_data(data)

        # Step 3: Validate datasets and relationships
        log_pipeline_step(logger, "Validating datasets")

        validation_results = validate_all_tables(cleaned_data)

        logger.info("Validation results: %s", validation_results)

        if isinstance(validation_results, dict):
            validation_failed = any(
                value is False for value in validation_results.values()
            )
            if validation_failed:
                raise ValueError("Dataset validation failed.")

        # Step 4: Save cleaned datasets
        log_pipeline_step(logger, "Saving cleaned datasets")

        CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        save_cleaned_data(cleaned_data, CLEANED_DATA_DIR)

        # Step 5: Calculate business KPIs
        log_pipeline_step(logger, "Calculating insurance KPIs")

        kpi_results = analyze_business(cleaned_data)

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        kpi_file = REPORTS_DIR / "business_kpis.txt"

        with kpi_file.open("w", encoding="utf-8") as file:
            file.write("MOTOR INSURANCE BUSINESS KPIs\n")
            file.write("=" * 40 + "\n\n")

            for section, results in kpi_results.items():
                file.write(f"{section.upper()}\n")
                file.write("-" * 30 + "\n")
                file.write(f"{results}\n\n")

        logger.info("Business KPIs saved to %s", kpi_file)

        # Step 6: Generate business insights
        log_pipeline_step(logger, "Generating business insights")

        insight_functions = [
            ("Portfolio Insights", generate_portfolio_insights),
            ("Claim Insights", generate_claim_insights),
            ("Premium Insights", generate_premium_insights),
            ("Customer Insights", generate_customer_insights),
            ("Vehicle Insights", generate_vehicle_insights),
            ("Risk Patterns", generate_risk_patterns),
            ("Business Recommendations", generate_business_recommendations),
        ]

        insight_file = REPORTS_DIR / "business_insights.txt"

        with insight_file.open("w", encoding="utf-8") as file:
            file.write("MOTOR INSURANCE BUSINESS INSIGHTS\n")
            file.write("=" * 40 + "\n\n")

            for title, insight_function in insight_functions:
                file.write(f"{title}\n")
                file.write("-" * 30 + "\n")

                try:
                    result = insight_function(cleaned_data)
                    file.write(f"{result}\n\n")
                except Exception as error:
                    logger.exception("Failed to generate %s", title)
                    file.write(f"Could not generate this section: {error}\n\n")

        # Step 7: Generate and save visualizations
        log_pipeline_step(logger, "Generating visualizations")

        chart_functions = [
            ("policy_status", plot_policy_status),
            ("policy_type_distribution", plot_policy_type_distribution),
            ("premium_by_policy_type", plot_premium_by_policy_type),
            ("monthly_claims", plot_monthly_claims),
            ("claim_status", plot_claim_status),
            ("claim_type_distribution", plot_claim_type_distribution),
            ("claim_amount_distribution", plot_claim_amount_distribution),
            ("claim_amount_by_vehicle_type", plot_claim_amount_by_vehicle_type),
            ("claims_by_region", plot_claims_by_region),
            ("claim_severity_by_region", plot_claim_severity_by_region),
            ("average_settlement_time", plot_average_settlement_time),
            ("claim_to_premium_by_policy_type", plot_claim_to_premium_by_policy_type),
            ("vehicle_age_vs_claim_amount", plot_vehicle_age_vs_claim_amount),
            ("customer_age_vs_claim_amount", plot_customer_age_vs_claim_amount),
            ("vehicle_type_claim_performance", plot_vehicle_type_claim_performance),
            ("damage_severity_distribution", plot_damage_severity_distribution),
            ("payment_status", plot_payment_status),
            ("monthly_premium_trend", plot_monthly_premium_trend),
        ]

        chart_count = 0

        for chart_name, chart_function in chart_functions:
            try:
                figure = chart_function(cleaned_data)

                if figure is not None:
                    figure.savefig(
                        REPORTS_DIR / f"{chart_name}.png",
                        bbox_inches="tight",
                        dpi=150,
                    )

                    # Close the figure to release memory.
                    import matplotlib.pyplot as plt

                    plt.close(figure)
                    chart_count += 1

            except Exception:
                logger.exception("Failed to generate chart: %s", chart_name)

        logger.info("Saved %s visualization charts", chart_count)

        # Step 8: Complete
        log_pipeline_step(logger, "Motor insurance analytics pipeline completed")

        print("\nMotor Insurance Analytics pipeline completed successfully.")
        print(f"Cleaned datasets: {CLEANED_DATA_DIR}")
        print(f"Business reports:  {REPORTS_DIR}")
        print(f"Execution logs:    {LOGS_DIR}")

        return {
            "status": "success",
            "kpis": kpi_results,
            "charts_generated": chart_count,
        }

    except Exception as error:
        log_exception(logger, error)
        print(f"\nPipeline failed: {error}")
        raise


if __name__ == "__main__":
    run_pipeline()


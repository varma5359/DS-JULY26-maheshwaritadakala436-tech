# Motor Insurance Analytics

**A Data Analytics and Business Intelligence Project for Motor Insurance**

## 1. Project Overview

Motor Insurance Analytics is a data analytics project designed to analyze motor insurance business operations using Python, Pandas, NumPy, Matplotlib, and Seaborn.

The project works with multiple related datasets to understand insurance customers, policies, vehicles, claims, and payments. It transforms raw data into meaningful business insights that help insurance companies monitor performance, identify risk patterns, and make data-driven decisions.

## 2. Business Objectives

* Analyze the insurance policy portfolio and policy status.
* Understand premium collection and revenue trends.
* Analyze claim frequency, claim amounts, and claim status.
* Measure claim settlement time and payment performance.
* Identify customer and vehicle-related risk patterns.
* Compare claims and premiums across policy types and regions.
* Generate actionable business recommendations.

## 3. Datasets

The project uses five related datasets.

| Dataset   | Purpose                                            |
| --------- | -------------------------------------------------- |
| Customers | Customer information and demographics              |
| Policies  | Policy details, coverage, premium, and status      |
| Vehicles  | Vehicle type, age, and value                       |
| Claims    | Claim amount, type, status, and settlement details |
| Payments  | Premium and claim-related payment information      |

The datasets are connected using customer IDs, policy IDs, vehicle IDs, claim IDs, and other relevant keys.

**Note:** The exact column names depend on the supplied CSV schema.

## 4. Technologies Used

* **Python** — Core programming language
* **Pandas** — Data manipulation and analysis
* **NumPy** — Numerical operations
* **Matplotlib** — Data visualization
* **Seaborn** — Statistical visualization
* **Pytest** — Automated testing
* **Logging** — Pipeline execution tracking
* **Docker** — Containerization

## 5. Project Structure

```text
motor-insurance-analytics/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── validation.py
│   ├── insurance_analysis.py
│   ├── insights.py
│   ├── visualization.py
│   └── logger.py
│
├── tests/
│   ├── test_pipeline.py
│   ├── test_analysis.py
│   └── test_validation.py
│
├── reports/
├── logs/
├── notebooks/
├── app/
│
├── run_pipeline.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## 6. Module Descriptions

### `data_loader.py`

* Checks whether input files exist.
* Loads CSV files into Pandas DataFrames.
* Loads the five datasets for further processing.

### `data_cleaner.py`

* Handles missing values and duplicate records.
* Cleans text and date columns.
* Converts numeric columns into appropriate data types.
* Validates business rules.
* Creates derived columns such as customer age, vehicle age, and policy duration.
* Saves cleaned datasets.

### `validation.py`

* Checks required columns.
* Identifies missing and duplicate IDs.
* Validates relationships between datasets.
* Checks whether required datasets are available.

### `insurance_analysis.py`

Calculates business KPIs, including:

* Total and active policies
* Premium totals and averages
* Claim totals and claim status rates
* Average claim settlement time
* Claim-to-premium ratio
* Payment-to-claim ratio
* Customer and vehicle summaries

### `insights.py`

Generates portfolio, claim, premium, customer, vehicle, and risk insights, along with business recommendations.

### `visualization.py`

Creates charts for policy distribution, premiums, claim trends, claim amounts, regional patterns, settlement time, customer and vehicle analysis, and payment status.

### `logger.py`

Configures logging to track pipeline execution, warnings, errors, and exceptions.

## 7. Installation

### Step 1: Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd motor-insurance-analytics
```

Replace the placeholder with your actual GitHub repository URL.

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you need to install the core packages manually:

```bash
pip install pandas numpy matplotlib seaborn pytest
```

## 8. Data Setup

Place the five source CSV files in the `data/raw/` directory.

Example:

```text
data/
└── raw/
    ├── customers.csv
    ├── policies.csv
    ├── vehicles.csv
    ├── claims.csv
    └── payments.csv
```

Ensure the file names match the names expected by `data_loader.py`.

## 9. Run the Project

From the project root, execute:

```bash
python run_pipeline.py
```

The intended pipeline workflow is:

1. Load the raw datasets.
2. Clean and transform the data.
3. Validate columns, IDs, and relationships.
4. Calculate insurance business KPIs.
5. Generate business insights.
6. Create visualizations.
7. Save applicable outputs and execution logs.

**Implementation note:** Ensure `run_pipeline.py` calls each required module and that output paths match your configuration.

## 10. Run Automated Tests

Run all tests:

```bash
python -m pytest tests/ -v
```

Run individual test files:

```bash
python -m pytest tests/test_pipeline.py -v
python -m pytest tests/test_analysis.py -v
python -m pytest tests/test_validation.py -v
```

The tests cover data loading, cleaning, analysis calculations, schema validation, and relationships between datasets.

## 11. Docker Setup

Build the Docker image:

```bash
docker build -t motor-insurance-analytics .
```

Run the container:

```bash
docker run --rm motor-insurance-analytics
```

The Dockerfile is configured to execute `run_pipeline.py` when the container starts.

Ensure that your raw datasets are available inside the container and that the pipeline writes outputs to the expected directories.

## 12. Business KPIs

| KPI                     | Business purpose                              |
| ----------------------- | --------------------------------------------- |
| Total Policies          | Measures portfolio size                       |
| Active Policy Rate      | Measures the proportion of active policies    |
| Total Premium           | Measures premium volume                       |
| Average Premium         | Compares average premium per policy           |
| Total Claims            | Measures claim volume                         |
| Average Claim Amount    | Measures average claim cost                   |
| Claim-to-Premium Ratio  | Compares claim amounts with premiums          |
| Average Settlement Time | Measures claim processing efficiency          |
| Payment-to-Claim Ratio  | Compares recorded payments with claim amounts |

KPI definitions should use consistent business rules, dates, statuses, and aggregation levels.

## 13. Business Questions

The analysis is designed to help answer questions such as:

* Which policy types contribute the most premium?
* How many policies are currently active?
* Which claim categories have higher claim amounts?
* Which regions report higher claim volumes?
* How long do claims take to settle?
* How do vehicle age and type relate to claim amounts?
* How do recorded claim payments compare with claim amounts?
* What operational improvements could reduce settlement delays?

These questions support business analysis and reporting; they do not automatically establish causation or predict future outcomes.

## 14. Expected Outputs

Depending on the implemented pipeline, outputs may include:

* Cleaned CSV datasets
* Summary KPI results
* Business insight reports
* Data visualization charts
* Pipeline execution logs
* Automated test results

Actual output files depend on the implementation of `run_pipeline.py` and the configured output paths.

## 15. Data Privacy

Insurance datasets may contain personally identifiable or commercially sensitive information.

* Do not commit real customer data to a public repository.
* Do not commit passwords, API keys, or production credentials.
* Use synthetic, anonymized, or approved sample datasets for demonstrations.
* Review `.gitignore` and `.dockerignore` before sharing the project.

## 16. Future Enhancements

Potential extensions include:

* An interactive Streamlit dashboard
* Scheduled analytics pipeline execution
* Database integration
* Automated report generation
* Cloud deployment
* Additional data quality checks

These are possible future improvements, not claims that the features are already implemented.

## 17. Project Summary

Motor Insurance Analytics demonstrates an end-to-end data analytics workflow, from loading and cleaning relational datasets to validating data, calculating business KPIs, generating insights, visualizing trends, and testing Python modules.

The primary goal is to convert insurance operational data into clear, useful information that supports business decision-making.

**Project Category:** Data Analytics / Business Analytics

**Core Focus:** Data Cleaning, EDA, KPI Analysis, Business Insights, Visualization, Testing, and Docker

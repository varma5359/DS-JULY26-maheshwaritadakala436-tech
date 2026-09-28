@echo off

echo ==========================================
echo Creating Logistics Delivery Analytics Project
echo ==========================================

mkdir logistics_delivery_analytics
cd logistics_delivery_analytics

mkdir data
mkdir data\raw
mkdir data\cleaned
mkdir notebooks
mkdir src
mkdir app
mkdir reports
mkdir tests

type nul > src\__init__.py
type nul > src\data_loader.py
type nul > src\data_cleaner.py
type nul > src\business_analysis.py
type nul > src\visualization.py

type nul > app\streamlit_app.py

type nul > reports\business_report.md

type nul > tests\test_pipeline.py

type nul > run_pipeline.py
type nul > requirements.txt
type nul > README.md
type nul > .gitignore

echo.
echo ==========================================
echo Project structure created successfully!
echo ==========================================

tree /F

pause
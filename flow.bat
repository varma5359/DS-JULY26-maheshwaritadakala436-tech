@echo off
setlocal
title Motor Insurance Analytics - Project Structure

REM Run this file from the location where you want the project folder created.
set "PROJECT=motor_insurance_analytics"

echo.
echo Creating project structure: %PROJECT%
echo.

REM Main folders
if not exist "%PROJECT%\data\raw" mkdir "%PROJECT%\data\raw"
if not exist "%PROJECT%\data\cleaned" mkdir "%PROJECT%\data\cleaned"
if not exist "%PROJECT%\notebooks" mkdir "%PROJECT%\notebooks"
if not exist "%PROJECT%\src" mkdir "%PROJECT%\src"
if not exist "%PROJECT%\app" mkdir "%PROJECT%\app"
if not exist "%PROJECT%\reports" mkdir "%PROJECT%\reports"
if not exist "%PROJECT%\tests" mkdir "%PROJECT%\tests"
if not exist "%PROJECT%\logs" mkdir "%PROJECT%\logs"

REM Python source modules required by the specification
if not exist "%PROJECT%\src\__init__.py" type nul > "%PROJECT%\src\__init__.py"
if not exist "%PROJECT%\src\data_loader.py" type nul > "%PROJECT%\src\data_loader.py"
if not exist "%PROJECT%\src\validation.py" type nul > "%PROJECT%\src\validation.py"
if not exist "%PROJECT%\src\data_cleaner.py" type nul > "%PROJECT%\src\data_cleaner.py"
if not exist "%PROJECT%\src\insurance_analysis.py" type nul > "%PROJECT%\src\insurance_analysis.py"
if not exist "%PROJECT%\src\visualization.py" type nul > "%PROJECT%\src\visualization.py"
if not exist "%PROJECT%\src\insights.py" type nul > "%PROJECT%\src\insights.py"
if not exist "%PROJECT%\src\logger.py" type nul > "%PROJECT%\src\logger.py"

REM Streamlit application
if not exist "%PROJECT%\app\streamlit_app.py" type nul > "%PROJECT%\app\streamlit_app.py"

REM Reports and tests
if not exist "%PROJECT%\reports\business_report.md" type nul > "%PROJECT%\reports\business_report.md"
if not exist "%PROJECT%\tests\test_pipeline.py" type nul > "%PROJECT%\tests\test_pipeline.py"
if not exist "%PROJECT%\tests\test_analysis.py" type nul > "%PROJECT%\tests\test_analysis.py"
if not exist "%PROJECT%\tests\test_validation.py" type nul > "%PROJECT%\tests\test_validation.py"

REM Root-level project files
if not exist "%PROJECT%\run_pipeline.py" type nul > "%PROJECT%\run_pipeline.py"
if not exist "%PROJECT%\requirements.txt" type nul > "%PROJECT%\requirements.txt"
if not exist "%PROJECT%\Dockerfile" type nul > "%PROJECT%\Dockerfile"
if not exist "%PROJECT%\.dockerignore" type nul > "%PROJECT%\.dockerignore"
if not exist "%PROJECT%\.gitignore" type nul > "%PROJECT%\.gitignore"
if not exist "%PROJECT%\README.md" type nul > "%PROJECT%\README.md"

REM Keep a copy of this setup script inside the project as well.
if not exist "%PROJECT%\flow.bat" copy "%~f0" "%PROJECT%\flow.bat" > nul

echo.
echo Project folders and placeholder files created successfully.
echo.
echo IMPORTANT:
echo 1. Add the five real CSV files into data\raw.
echo 2. Create notebooks\insurance_analysis.ipynb using Jupyter Notebook.
echo 3. Fill the Python modules with the required functions.
echo 4. This script does not create fake or empty CSV datasets.
echo.
echo Project location: %CD%\%PROJECT%
echo.
pause
endlocal

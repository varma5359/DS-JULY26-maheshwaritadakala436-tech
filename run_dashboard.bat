@echo off
setlocal

set "PROJECT_DIR=%~dp0logistics_delivery_analytics"

if not exist "%PROJECT_DIR%\app\streamlit_app.py" (
    echo Could not find the dashboard at "%PROJECT_DIR%\app\streamlit_app.py".
    exit /b 1
)

pushd "%PROJECT_DIR%"
"%~dp0.venv\Scripts\python.exe" -m streamlit run app\streamlit_app.py
set "EXIT_CODE=%ERRORLEVEL%"
popd

exit /b %EXIT_CODE%
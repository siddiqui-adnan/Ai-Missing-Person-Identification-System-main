@echo off
REM Startup script for AI Missing Person Identification System
REM Checks dependencies and starts the application

REM Change to project root directory (parent of scripts folder)
cd /d "%~dp0.."

echo ============================================================
echo.
echo   AI Missing Person Identification System
echo   Starting Application...
echo.
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Streamlit not found
    echo.
    set /p response="Would you like to install dependencies now? (y/n): "
    if /i "%response%"=="y" (
        echo Installing dependencies...
        pip install -r requirements.txt
        if %errorlevel% neq 0 (
            echo [ERROR] Failed to install dependencies
            pause
            exit /b 1
        )
    ) else (
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM Check if Home.py exists
if not exist "Home.py" (
    echo [ERROR] Home.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Create necessary directories
if not exist "resources" mkdir resources
if not exist "backups" mkdir backups
if not exist "logs" mkdir logs

echo.
echo [OK] All checks passed
echo.
echo Starting application...
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

REM Start the application using python -m to avoid PATH issues
python -m streamlit run Home.py
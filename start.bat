@echo off
echo Starting Comic Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
if not exist "venv\installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo. > venv\installed
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your settings!
)

REM Create necessary directories
if not exist "data" mkdir data
if not exist "cache" mkdir cache
if not exist "static" mkdir static
if not exist "templates" mkdir templates

echo.
echo Setup complete!
echo.
echo Starting server at http://localhost:8000
echo API docs at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python main.py

pause

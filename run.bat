@echo off
echo =========================================
echo Chatbot Quan ly Thoi gian
echo =========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo =========================================
echo Starting server...
echo =========================================
echo.
echo Access application at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop server
echo.

REM Run the application
python main.py

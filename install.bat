@echo off
REM Dependency Installer for Mail Automation Tool
REM This script installs all required Python packages

echo.
echo ================================
echo Mail Automation Tool - Installer
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from: https://www.python.org/
    echo.
    echo During installation, make sure to:
    echo - Check "Add Python to PATH"
    echo - Check "Install pip"
    echo.
    pause
    exit /b 1
)

echo Found Python:
python --version
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Warning: Could not upgrade pip, continuing anyway...
)
echo.

REM Install requirements
echo Installing required packages...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install some packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ================================
echo Installation Complete!
echo ================================
echo.
echo Next steps:
echo 1. Download ChromeDriver from https://googlechromelabs.github.io/chrome-for-testing/
echo 2. Place chromedriver.exe in this folder OR system PATH
echo 3. Login to Gmail in Chrome browser
echo 4. Run: python main.py
echo.
pause

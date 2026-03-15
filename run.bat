@echo off
REM Mail Automation Tool Launcher
REM This batch file runs the mail automation tool

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Run the application (tkinter version - no extra dependencies)
echo.
echo Starting Mail Automation Tool...
echo.
python main_tkinter.py

if errorlevel 1 (
    echo.
    echo Error occurred while running the application
    echo Check logs folder for details
    pause
)

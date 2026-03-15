@echo off
REM Troubleshooting script for Chrome startup issues
REM This will diagnose and help fix Chrome problems

echo.
echo ================================
echo Chrome Troubleshooting Tool
echo ================================
echo.

cd /d "%~dp0"

echo Running detailed diagnostic...
echo.

python troubleshoot_chrome.py

echo.
echo ================================
echo Diagnostic Complete
echo ================================
echo.

if errorlevel 1 (
    echo ⚠️  Issues were found. Follow the solutions above.
) else (
    echo ✓ All checks passed!
)

echo.
echo Next step: python main_tkinter.py
echo.

pause

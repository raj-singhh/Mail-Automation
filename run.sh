#!/bin/bash
# Mail Automation Tool Launcher for Linux/Mac

cd "$(dirname "$0")"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org/"
    exit 1
fi

# Check if requirements are installed
python3 -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install requirements"
        echo "Please run: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# Run the application
echo ""
echo "Starting Mail Automation Tool..."
echo ""
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error occurred while running the application"
    echo "Check logs folder for details"
fi

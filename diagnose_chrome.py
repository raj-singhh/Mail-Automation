"""
Diagnostic tool to check Chrome and ChromeDriver setup
Run this to troubleshoot Chrome issues
"""
import os
import subprocess
import shutil
import sys

def check_chrome_installed():
    """Check if Chrome is installed"""
    print("\n" + "="*60)
    print("STEP 1: Check if Chrome is installed")
    print("="*60)
    
    chrome_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✓ Chrome found at: {path}")
            return path
    
    print("✗ Chrome not found")
    print("\nSolution: Download and install Chrome from https://www.google.com/chrome/")
    return None

def get_chrome_version(chrome_path):
    """Get installed Chrome version"""
    print("\n" + "="*60)
    print("STEP 2: Get your Chrome version")
    print("="*60)
    
    try:
        result = subprocess.run([chrome_path, "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✓ {version}")
        # Extract version number
        version_num = version.split()[-1].split('.')[0]
        return version_num
    except Exception as e:
        print(f"✗ Error getting Chrome version: {e}")
        return None

def check_chromedriver():
    """Check if ChromeDriver is available"""
    print("\n" + "="*60)
    print("STEP 3: Check for ChromeDriver")
    print("="*60)
    
    # Check in current directory
    if os.path.exists("chromedriver.exe"):
        print("✓ chromedriver.exe found in current folder")
        
        # Try to get version
        try:
            result = subprocess.run(["chromedriver.exe", "--version"], capture_output=True, text=True)
            version = result.stdout.strip()
            print(f"  Version: {version}")
            return True
        except:
            print("  (Could not determine version)")
            return True
    
    # Check in PATH
    if shutil.which("chromedriver"):
        print("✓ chromedriver found in system PATH")
        return True
    
    print("✗ ChromeDriver not found")
    return False

def main():
    print("\n" + "█"*60)
    print("Chrome Setup Diagnostic Tool")
    print("█"*60)
    
    # Step 1: Check Chrome
    chrome_path = check_chrome_installed()
    if not chrome_path:
        print("\n" + "!"*60)
        print("FATAL: Chrome is not installed")
        print("!"*60)
        return 1
    
    # Step 2: Get Chrome version
    chrome_version = get_chrome_version(chrome_path)
    if not chrome_version:
        return 1
    
    # Step 3: Check ChromeDriver
    has_chromedriver = check_chromedriver()
    
    if not has_chromedriver:
        print("\n" + "⚠️ "*30)
        print("CHROMEDRIVER MISSING!")
        print("⚠️ "*30)
        print(f"""
Your Chrome version: {chrome_version}

SOLUTION:
1. Visit: https://googlechromelabs.github.io/chrome-for-testing/
2. Find your Chrome version ({chrome_version}.x) in the table
3. Download: chromedriver.exe (Windows 64-bit)
4. Extract and save to: {os.getcwd()}\\chromedriver.exe

Then run the application again.
""")
        return 1
    
    print("\n" + "="*60)
    print("✓ All checks passed!")
    print("="*60)
    print(f"""
Chrome: ✓ Installed
Version: {chrome_version}
ChromeDriver: ✓ Found

You're ready to run the application!

Try: python main_tkinter.py
""")
    return 0

if __name__ == "__main__":
    sys.exit(main())

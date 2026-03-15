"""
Setup checker - Verifies all dependencies and configuration
Run this before first use: python check_setup.py
"""
import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required. Current: {}.{}".format(version.major, version.minor))
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        print(f"✓ {package_name} installed")
        return True
    except ImportError:
        print(f"❌ {package_name} not found. Install with: pip install {package_name}")
        return False

def check_chrome():
    """Check if Chrome is installed"""
    import shutil
    if shutil.which("chrome") or shutil.which("chrome.exe") or os.path.exists(
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    ):
        print("✓ Chrome browser found")
        return True
    print("❌ Chrome not found. Please install Google Chrome")
    return False

def check_chromedriver():
    """Check if ChromeDriver is available"""
    import shutil
    if shutil.which("chromedriver") or shutil.which("chromedriver.exe") or os.path.exists("chromedriver.exe"):
        print("✓ ChromeDriver found")
        return True
    print("⚠️  ChromeDriver not found in PATH. Download from:")
    print("    https://googlechromelabs.github.io/chrome-for-testing/")
    print("    and place in project folder or system PATH")
    return False

def check_directories():
    """Check if required directories exist"""
    dirs = ["logs", "email_templates", "config"]
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"✓ Directory '{dir_name}' exists")
        else:
            os.makedirs(dir_name)
            print(f"✓ Created directory '{dir_name}'")
    return True

def main():
    print("\n" + "="*50)
    print("Mail Automation Tool - Setup Checker")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Chrome Browser", check_chrome),
        ("PyQt5 Package", lambda: check_package("PyQt5")),
        ("Selenium Package", lambda: check_package("selenium")),
        ("python-dotenv Package", lambda: check_package("dotenv")),
        ("ChromeDriver", check_chromedriver),
        ("Directories", check_directories),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\nChecking {check_name}...")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error checking {check_name}: {str(e)}")
            results.append((check_name, False))
    
    print("\n" + "="*50)
    print("Setup Check Summary")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✓ Passed" if result else "❌ Failed"
        print(f"{check_name:30} {status}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ All checks passed! You're ready to use the tool.")
        print("\nRun: python main.py")
        return 0
    else:
        print("\n⚠️  Some checks failed. Review errors above and fix them.")
        print("\nMost Common Issues:")
        print("1. Missing dependencies: pip install -r requirements.txt")
        print("2. Chrome not installed: Download from https://www.google.com/chrome/")
        print("3. ChromeDriver mismatch: Match version with your Chrome version")
        return 1

if __name__ == "__main__":
    sys.exit(main())

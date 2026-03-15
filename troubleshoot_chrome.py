"""
Advanced Chrome Launch Troubleshooting Tool
Help diagnose and fix Chrome startup issues
"""
import os
import subprocess
import sys
from pathlib import Path
import logging
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_step(step_num, description):
    print(f"\n[STEP {step_num}] {description}")
    print("-" * 70)

def check_chrome_path():
    """Verify Chrome executable exists"""
    print_step(1, "Check Chrome Installation Path")
    
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    if os.path.exists(chrome_path):
        print(f"✓ Chrome found at: {chrome_path}")
        
        # Get file info
        file_size = os.path.getsize(chrome_path) / (1024*1024)
        print(f"✓ File size: {file_size:.1f} MB")
        
        return chrome_path
    else:
        print(f"✗ Chrome NOT found at: {chrome_path}")
        
        # Try alternative paths
        alternatives = [
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
        ]
        
        for alt_path in alternatives:
            if os.path.exists(alt_path):
                print(f"✓ Found at alternative location: {alt_path}")
                return alt_path
        
        print("✗ Chrome not found in any standard location")
        return None

def check_chromedriver_path():
    """Verify ChromeDriver exists"""
    print_step(2, "Check ChromeDriver Location")
    
    paths_to_check = [
        os.path.join(os.getcwd(), 'chromedriver.exe'),
        'chromedriver.exe',
        os.path.expandvars(r'%PATH%'),
    ]
    
    for path in paths_to_check:
        if os.path.isfile(path):
            abs_path = os.path.abspath(path)
            print(f"✓ ChromeDriver found at: {abs_path}")
            
            # Check file size
            file_size = os.path.getsize(abs_path) / (1024*1024)
            print(f"✓ File size: {file_size:.1f} MB")
            
            return abs_path
        elif os.path.isdir(path):
            # Check if chromedriver.exe is in PATH directory
            chromedriver = os.path.join(path, 'chromedriver.exe')
            if os.path.exists(chromedriver):
                print(f"✓ ChromeDriver found in PATH: {chromedriver}")
                return chromedriver
    
    print(f"✗ ChromeDriver not found")
    print(f"  Checked paths:")
    for path in paths_to_check:
        print(f"    - {path}")
    return None

def check_chrome_user_data():
    """Check Chrome user data directory"""
    print_step(3, "Check Chrome User Data Directory")
    
    username = os.getenv('USERNAME')
    user_data_dir = f'C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data'
    
    print(f"Username: {username}")
    print(f"Chrome User Data: {user_data_dir}")
    
    if os.path.exists(user_data_dir):
        print(f"✓ User data directory exists")
        
        # List profiles
        profile_dirs = []
        if os.path.exists(os.path.join(user_data_dir, 'Default')):
            profile_dirs.append('Default')
        
        for item in os.listdir(user_data_dir):
            if item.startswith('Profile '):
                profile_dirs.append(item)
        
        if profile_dirs:
            print(f"✓ Found {len(profile_dirs)} Chrome profile(s):")
            for profile in profile_dirs:
                print(f"    - {profile}")
            return user_data_dir
        else:
            print(f"⚠️  No Chrome profiles found (Chrome may not have been run yet)")
            return user_data_dir
    else:
        print(f"✗ User data directory does NOT exist")
        print(f"✗ Chrome may not have been configured properly")
        return None

def check_chrome_process():
    """Check if Chrome is already running"""
    print_step(4, "Check for Running Chrome Processes")
    
    try:
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq chrome.exe'],
            capture_output=True,
            text=True
        )
        
        if 'chrome.exe' in result.stdout:
            lines = result.stdout.strip().split('\n')
            print(f"⚠️  Chrome is currently running:")
            for line in lines:
                if 'chrome.exe' in line:
                    print(f"    {line}")
            print(f"\n⚠️  Solution: Close all Chrome windows and try again")
            return True
        else:
            print(f"✓ Chrome is not currently running (good)")
            return False
    except Exception as e:
        print(f"⚠️  Could not check Chrome processes: {e}")
        return None

def test_chrome_launch(chrome_path):
    """Test launching Chrome"""
    print_step(5, "Test Launch Chrome")
    
    if not chrome_path:
        print("✗ Chrome path not available, skipping launch test")
        return False
    
    try:
        print(f"Launching Chrome for 3 seconds...")
        process = subprocess.Popen(
            [chrome_path, '--test-type'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(3)
        
        if process.poll() is None:
            print("✓ Chrome launched successfully")
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            returncode = process.returncode
            stdout, stderr = process.communicate()
            print(f"✗ Chrome failed to start (exit code: {returncode})")
            if stderr:
                print(f"Error: {stderr.decode()[:200]}")
            return False
            
    except Exception as e:
        print(f"✗ Error testing Chrome launch: {e}")
        return False

def test_selenium_import():
    """Test if Selenium is installed correctly"""
    print_step(6, "Test Selenium Installation")
    
    try:
        from selenium import webdriver
        print("✓ Selenium imported successfully")
        
        # Check version
        import selenium
        print(f"✓ Selenium version: {selenium.__version__}")
        
        return True
    except ImportError as e:
        print(f"✗ Failed to import Selenium: {e}")
        print(f"Solution: Run: pip install selenium==4.11.2")
        return False

def provide_solutions(results):
    """Provide solutions based on test results"""
    print_header("TROUBLESHOOTING SOLUTIONS")
    
    chrome_found, chromedriver_found, user_data_ok, chrome_running, selenium_ok = results
    
    if not chrome_found:
        print("\n❌ ISSUE: Chrome not found")
        print("SOLUTIONS:")
        print("  1. Install Google Chrome from https://google.com/chrome")
        print("  2. Make sure it's installed in the default location:")
        print("     C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    
    if not chromedriver_found:
        print("\n❌ ISSUE: ChromeDriver not found")
        print("SOLUTIONS:")
        print("  1. Download ChromeDriver matching your Chrome version")
        print("  2. Visit: https://googlechromelabs.github.io/chrome-for-testing/")
        print("  3. Download version 146.0.7680.66")
        print("  4. Extract chromedriver.exe to this folder:")
        print(f"     {os.getcwd()}")
    
    if not user_data_ok:
        print("\n❌ ISSUE: Chrome user data directory not found")
        print("SOLUTIONS:")
        print("  1. Open Chrome normally and log in")
        print("  2. Close all Chrome windows")
        print("  3. Try running the tool again")
    
    if chrome_running:
        print("\n❌ ISSUE: Chrome is already running")
        print("SOLUTIONS:")
        print("  1. Close ALL Chrome windows (including background)")
        print("  2. Use Task Manager if needed (Ctrl+Shift+Esc)")
        print("  3. Try running the tool again")
    
    if not selenium_ok:
        print("\n❌ ISSUE: Selenium not properly installed")
        print("SOLUTIONS:")
        print("  1. Run: pip install --upgrade selenium==4.11.2")
        print("  2. Or double-click: install.bat")
    
    # Overall status
    if all(results):
        print("\n" + "="*70)
        print("✓ ALL CHECKS PASSED!")
        print("="*70)
        print("\nYou should now be able to run:")
        print("  python main_tkinter.py")
        print("\nIf you still get errors, check the logs:")
        print("  logs/mail_automation.log")
    else:
        print("\n" + "="*70)
        print("⚠️  SOME ISSUES FOUND - Please fix above and try again")
        print("="*70)

def main():
    print_header("CHROME TROUBLESHOOTING DIAGNOSTIC")
    
    results = []
    
    # Run all checks
    chrome_path = check_chrome_path()
    results.append(chrome_path is not None)
    
    chromedriver_path = check_chromedriver_path()
    results.append(chromedriver_path is not None)
    
    user_data = check_chrome_user_data()
    results.append(user_data is not None)
    
    chrome_running = check_chrome_process()
    results.append(not chrome_running)  # We want it to NOT be running
    
    if chrome_path and not chrome_running:
        selenium_ok = test_selenium_import()
        results.append(selenium_ok)
        
        if selenium_ok and chromedriver_path:
            test_chrome_launch(chrome_path)
    else:
        test_selenium_import()
        results.append(False)
    
    # Provide solutions
    provide_solutions(results)
    
    print_header("NEXT STEPS")
    print("\nOption 1: Run the GUI application")
    print("  python main_tkinter.py")
    print("\nOption 2: Click 'Test Chrome' button in the GUI")
    print("  This will diagnose Chrome issues without sending emails")
    print("\nOption 3: Check the logs for detailed error messages")
    print("  Open: logs/mail_automation.log")

if __name__ == '__main__':
    main()

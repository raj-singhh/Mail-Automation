#!/usr/bin/env python3
"""
Mail Automation Tool - Setup & Installation Script
This script guides you through the complete setup process
"""
import os
import sys
import subprocess
import platform

def print_header(text):
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60 + "\n")

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"▶ {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} - Success!")
            return True
        else:
            print(f"✗ {description} - Failed!")
            if result.stderr:
                print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {description} - Error: {str(e)}")
        return False

def main():
    print_header("Mail Automation Tool - Complete Setup")
    
    os_type = platform.system()
    print(f"Detected OS: {os_type}\n")
    
    # Check Python
    print("1️⃣  CHECKING PYTHON")
    print("-" * 60)
    result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
    print(result.stdout)
    
    # Check/Install dependencies
    print("\n2️⃣  INSTALLING DEPENDENCIES")
    print("-" * 60)
    
    if os_type == "Windows":
        cmd = "pip install -r requirements.txt"
    else:
        cmd = "pip3 install -r requirements.txt"
    
    if run_command(cmd, "Installing Python packages"):
        print("✓ All Python packages installed!")
    else:
        print("✗ Failed to install packages")
        print("Try manually running: pip install -r requirements.txt")
        return 1
    
    # Verify installation
    print("\n3️⃣  VERIFYING INSTALLATION")
    print("-" * 60)
    
    required_packages = ["PyQt5", "selenium"]
    all_ok = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} - OK")
        except ImportError:
            print(f"✗ {package} - Missing")
            all_ok = False
    
    if not all_ok:
        print("\n✗ Some packages are missing!")
        return 1
    
    # ChromeDriver notice
    print("\n4️⃣  CHROMEDRIVER SETUP")
    print("-" * 60)
    print("⚠️  ChromeDriver is required to automate Chrome")
    print("\nSteps:")
    print("1. Find your Chrome version:")
    print("   - Open Chrome → ⋮ Menu → Help → About Google Chrome")
    print("   - Note the version (e.g., 120.0.6099.00)")
    print("\n2. Download matching ChromeDriver from:")
    print("   https://googlechromelabs.github.io/chrome-for-testing/")
    print("\n3. Extract the executable to:")
    print("   - Project folder (same as main.py), OR")
    print("   - Add to system PATH")
    print("\n4. Verify by running: chromedriver --version")
    
    # Gmail setup notice
    print("\n5️⃣  GMAIL SETUP")
    print("-" * 60)
    print("✓ Open Google Chrome")
    print("✓ Go to: https://gmail.com")
    print("✓ Login with your email account")
    print("✓ Keep this window open while using the tool")
    
    # Test optional
    print("\n6️⃣  RUN TESTS (Optional)")
    print("-" * 60)
    test_choice = input("Run test suite to verify everything? (yes/no): ").strip().lower()
    
    if test_choice == 'yes':
        if os_type == "Windows":
            cmd = "python test_tool.py"
        else:
            cmd = "python3 test_tool.py"
        
        os.system(cmd)
    
    # Success
    print_header("✓ Setup Complete!")
    
    print("Next Steps:")
    print("1. Make sure Chrome is open and logged into Gmail")
    print("2. Run the application:")
    
    if os_type == "Windows":
        print("   - Double-click: run.bat")
        print("   - Or: python main.py")
    else:
        print("   - bash run.sh")
        print("   - Or: python3 main.py")
    
    print("\n3. Follow the in-app instructions:")
    print("   ① Paste email addresses")
    print("   ② Write subject and body")
    print("   ③ Select resume (optional)")
    print("   ④ Preview emails")
    print("   ⑤ Click Send!")
    
    print("\n📚 Documentation:")
    print("   - README.md - Full documentation")
    print("   - QUICKSTART.md - Quick start guide")
    print("   - START_HERE.md - Overview")
    
    print("\n" + "="*60)
    print("Ready to automate your emails! 🚀")
    print("="*60 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

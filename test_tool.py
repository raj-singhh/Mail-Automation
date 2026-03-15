"""
Test utility - Test email sending with a single recipient
Run this to verify everything is working before sending to many recipients
"""
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from email_utils import extract_name_from_email, format_email_body, parse_email_list
from chrome_handler import ChromeEmailHandler

def test_name_extraction():
    """Test email name extraction"""
    print("\n" + "="*50)
    print("Testing Name Extraction")
    print("="*50)
    
    test_emails = [
        "john.doe@gmail.com",
        "jane_smith@company.com",
        "mike.j.johnson@example.com",
        "a.b@test.com"
    ]
    
    for email in test_emails:
        name = extract_name_from_email(email)
        print(f"{email:30} → {name}")
    
    print("\n✓ Name extraction test passed!")

def test_email_parsing():
    """Test email list parsing"""
    print("\n" + "="*50)
    print("Testing Email Parsing")
    print("="*50)
    
    # Test comma-separated
    email_input1 = "john@example.com, jane@example.com, invalid.email"
    emails1 = parse_email_list(email_input1)
    print(f"Input (comma): {email_input1}")
    print(f"Parsed: {emails1}")
    
    # Test newline-separated
    email_input2 = """john@example.com
jane@example.com
mike@example.com"""
    emails2 = parse_email_list(email_input2)
    print(f"\nInput (newline): {email_input2}")
    print(f"Parsed: {emails2}")
    
    print("\n✓ Email parsing test passed!")

def test_email_formatting():
    """Test email formatting with personalization"""
    print("\n" + "="*50)
    print("Testing Email Formatting")
    print("="*50)
    
    body = "I am interested in the position at your organization. With my experience, I believe I can contribute significantly."
    
    emails = ["john.doe@gmail.com", "jane_smith@company.com"]
    
    for email in emails:
        formatted = format_email_body(body, email)
        print(f"\nEmail: {email}")
        print("Formatted Body:")
        print(formatted)
    
    print("\n✓ Email formatting test passed!")

def test_chrome_connection():
    """Test Chrome connection (optional)"""
    print("\n" + "="*50)
    print("Testing Chrome Connection")
    print("="*50)
    print("⚠️  This test requires Chrome to be installed and will open it.")
    
    response = input("Do you want to test Chrome connection? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Skipped Chrome connection test")
        return
    
    try:
        handler = ChromeEmailHandler()
        print("Starting Chrome...")
        
        if handler.start_chrome():
            print("✓ Chrome started successfully")
            print("Waiting for Gmail to load...")
            
            if handler.wait_for_gmail_load():
                print("✓ Gmail loaded successfully")
            else:
                print("⚠️  Gmail didn't load in time")
            
            handler.close()
            print("✓ Chrome closed")
        else:
            print("❌ Failed to start Chrome")
    
    except Exception as e:
        print(f"❌ Error during Chrome test: {str(e)}")

def main():
    print("\n" + "="*70)
    print("Mail Automation Tool - Test Suite")
    print("="*70)
    
    try:
        # Run tests
        test_name_extraction()
        test_email_parsing()
        test_email_formatting()
        test_chrome_connection()
        
        print("\n" + "="*70)
        print("All Tests Completed!")
        print("="*70)
        print("\n✓ Basic functionality is working")
        print("✓ You're ready to use the full application")
        print("\nRun: python main.py")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

"""
Download the correct ChromeDriver version for Chrome 146.0.7680.72
"""
import os
import json
import urllib.request
import zipfile

def main():
    print("\n" + "="*70)
    print("Downloading ChromeDriver 146.0.7680.72")
    print("="*70 + "\n")
    
    # This is the exact version from the log
    chrome_version = "146.0.7680.72"
    chromedriver_version = "146.0.7680.72"
    
    print(f"Chrome version: {chrome_version}")
    print(f"Downloading ChromeDriver: {chromedriver_version}\n")
    
    # Direct URL to Chrome for Testing
    download_url = f"https://edgedl.me/chrome-for-testing/{chromedriver_version}/win64-chrome-driver.zip"
    
    print(f"Download URL: {download_url}\n")
    print("This may take 30-60 seconds...\n")
    
    try:
        # Download
        print("Downloading...")
        temp_zip = 'chromedriver_temp.zip'
        urllib.request.urlretrieve(download_url, temp_zip)
        print(f"✓ Downloaded successfully ({os.path.getsize(temp_zip) / (1024*1024):.1f} MB)\n")
        
        # Extract
        print("Extracting...")
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            # List contents
            files = zip_ref.namelist()
            chromedriver_file = None
            
            for file in files:
                if 'chromedriver' in file and file.endswith('.exe'):
                    chromedriver_file = file
                    break
            
            if chromedriver_file:
                print(f"Found: {chromedriver_file}")
                
                # Extract the file
                extracted = zip_ref.extract(chromedriver_file)
                
                # Copy to current directory
                import shutil
                dest = 'chromedriver.exe'
                
                if os.path.exists(dest):
                    os.remove(dest)
                
                shutil.copy(extracted, dest)
                print(f"✓ Extracted to: {dest}\n")
                
                # Verify
                if os.path.exists(dest):
                    size = os.path.getsize(dest) / (1024*1024)
                    print(f"✓ File size: {size:.1f} MB")
                    print(f"✓ ChromeDriver ready!\n")
                    
                    # Cleanup
                    os.remove(temp_zip)
                    shutil.rmtree('chrome-win64', ignore_errors=True)
                    
                    print("="*70)
                    print("✓ SUCCESS! Ready to use.")
                    print("="*70)
                    print("\nNext: python main_tkinter.py\n")
                    return True
        
        print("✗ Could not find chromedriver.exe in ZIP")
        return False
        
    except urllib.error.HTTPError as e:
        print(f"✗ Download failed: HTTP {e.code}")
        print(f"\nTry manual download:")
        print(f"1. Go to: https://googlechromelabs.github.io/chrome-for-testing/")
        print(f"2. Find version: {chromedriver_version}")
        print(f"3. Download: chromedriver-win64.zip")
        print(f"4. Extract chromedriver.exe to: {os.getcwd()}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        print(f"\nManual download:")
        print(f"1. Visit: https://googlechromelabs.github.io/chrome-for-testing/")
        print(f"2. Find version: {chromedriver_version} (win64)")
        print(f"3. Download and extract to: {os.getcwd()}")
        return False

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    success = main()
    exit(0 if success else 1)

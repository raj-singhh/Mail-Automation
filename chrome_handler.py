"""
Chrome automation handler for sending emails
Uses Selenium WebDriver to automate Gmail interface
"""
import time
import os
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)

class ChromeEmailHandler:
    def __init__(self, headless=False):
        """
        Initialize Chrome WebDriver
        
        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.driver = None
        self.wait = None
        
    def start_chrome(self):
        """
        Start Chrome WebDriver with Gmail
        """
        options = webdriver.ChromeOptions()
        
        # Important: Don't use user profile - it causes dialog interruptions
        # Chrome will ask which profile to use, which breaks automation
        logger.info("Configuring Chrome options...")
        
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-web-resources')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-extensions')
        
        # Disable notification prompts
        options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2
        })
        
        logger.info("Initializing Chrome WebDriver...")
        
        try:
            # Find ChromeDriver
            chromedriver_path = None
            search_paths = [
                'chromedriver.exe',
                os.path.join(os.getcwd(), 'chromedriver.exe'),
                os.path.join(os.path.dirname(__file__), 'chromedriver.exe'),
            ]
            
            for path in search_paths:
                if os.path.exists(path):
                    chromedriver_path = os.path.abspath(path)
                    logger.info(f"Found ChromeDriver at: {chromedriver_path}")
                    break
            
            if not chromedriver_path:
                logger.warning("ChromeDriver not found in common locations, trying PATH...")
            
            # Initialize driver - simple and direct
            if chromedriver_path:
                logger.info(f"Using ChromeDriver: {chromedriver_path}")
                service = Service(chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                logger.info("Using ChromeDriver from PATH")
                self.driver = webdriver.Chrome(options=options)
            
            logger.info("WebDriver initialized successfully")
            
            # Set timeout
            self.driver.set_page_load_timeout(20)
            self.wait = WebDriverWait(self.driver, 20)
            
            # Navigate to Gmail  
            logger.info("Navigating to Gmail...")
            self.driver.get('https://gmail.com')
            
            logger.info("Chrome started successfully")
            return True
            
        except Exception as e:
            error_details = str(e)
            logger.error(f"Failed to start Chrome: {error_details}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Common solutions:")
            logger.error(f"1. Make sure you're logged into Gmail in Chrome BEFORE running this")
            logger.error(f"2. Check if Chrome is showing a profile selection dialog")
            logger.error(f"3. Close all Chrome windows completely and try again")
            logger.error(f"4. Verify ChromeDriver version matches Chrome version (both 146.0.7680.72)")
            logger.error(f"Download from: https://googlechromelabs.github.io/chrome-for-testing/")
            return False
    
    def wait_for_gmail_load(self, timeout=20):
        """
        Wait for Gmail to fully load
        """
        try:
            logger.info("Waiting for Gmail to load...")
            
            # Wait for Gmail inbox to be visible
            # Look for compose button or inbox elements
            self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "https://mail.google.com")]'))
            )
            
            logger.info("✓ Gmail loaded successfully")
            time.sleep(2)  # Extra time for full page load
            return True
            
        except TimeoutException:
            logger.error(f"⚠️  Gmail did not load within {timeout} seconds")
            logger.error("Make sure you are logged into Gmail in Chrome")
            logger.error("Try: Open Chrome manually and go to https://gmail.com, then login")
            return False
        except Exception as e:
            logger.error(f"Error waiting for Gmail: {str(e)}")
            return False
    
    def click_compose(self):
        """
        Click on the Compose button
        """
        try:
            logger.info("Looking for compose button...")
            
            # Multiple strategies to find compose button
            selectors = [
                '//div[@aria-label="Compose"]',
                '//div[@data-tooltip="Compose"]',
                '//a[@href="https://mail.google.com/mail/u/0/#compose"]',
                '//button[contains(@aria-label, "Compose")]'
            ]
            
            compose_button = None
            for selector in selectors:
                try:
                    element = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    compose_button = element
                    logger.info(f"✓ Found compose button with selector: {selector}")
                    break
                except:
                    continue
            
            if not compose_button:
                logger.error("Could not find compose button with any selector")
                return False
            
            compose_button.click()
            logger.info("Clicked compose button")
            time.sleep(2)
            return True
            
        except Exception as e:
            logger.error(f"Failed to click compose: {str(e)}")
            return False
    
    def fill_recipient(self, email):
        """
        Fill recipient email address
        """
        try:
            logger.info(f"Filling recipient: {email}")
            
            # Click on recipient field
            recipient_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//input[@aria-label="To"]'))
            )
            recipient_field.click()
            time.sleep(0.5)
            recipient_field.send_keys(email)
            logger.info(f"Typed recipient email")
            time.sleep(1)
            
            # Wait for suggestion and click first suggestion
            try:
                suggestion = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@role="option"]')),
                    timeout=3
                )
                suggestion.click()
                logger.info("Selected email suggestion")
            except:
                logger.info("No suggestion appeared, pressing Tab instead")
                recipient_field.send_keys(Keys.TAB)
            
            time.sleep(1)
            return True
            
        except Exception as e:
            logger.error(f"Failed to fill recipient: {str(e)}")
            return False
    
    def fill_subject(self, subject):
        """
        Fill email subject
        """
        try:
            logger.info(f"Filling subject: {subject[:30]}...")
            
            subject_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="subjectbox"]'))
            )
            subject_field.click()
            time.sleep(0.3)
            subject_field.send_keys(subject)
            logger.info("Subject filled")
            time.sleep(0.5)
            return True
            
        except Exception as e:
            logger.error(f"Failed to fill subject: {str(e)}")
            return False
    
    def fill_body(self, body):
        """
        Fill email body
        """
        try:
            logger.info(f"Filling body ({len(body)} characters)...")
            
            # Click on body area
            body_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Message body"]'))
            )
            body_field.click()
            time.sleep(0.5)
            
            # Type the body slowly to avoid issues
            for char in body:
                self.driver.find_element(By.XPATH, '//div[@aria-label="Message body"]').send_keys(char)
                time.sleep(0.01)  # Small delay between characters
            
            logger.info("Body filled")
            time.sleep(0.5)
            return True
            
        except Exception as e:
            logger.error(f"Failed to fill body: {str(e)}")
            return False
    
    def attach_file(self, file_path):
        """
        Attach a file (resume)
        """
        try:
            logger.info(f"Attaching file: {file_path}")
            
            # Click attach button
            attach_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Attach files"]')),
                timeout=5
            )
            attach_button.click()
            logger.info("Clicked attach button")
            time.sleep(1)
            
            # Send file path to file input
            file_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
            abs_path = os.path.abspath(file_path)
            logger.info(f"Sending file path: {abs_path}")
            file_input.send_keys(abs_path)
            time.sleep(3)  # Wait for upload
            logger.info("✓ File attached successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to attach file: {str(e)}")
            return False
    
    def close_compose(self):
        """
        Close the compose window
        """
        try:
            logger.info("Closing compose window...")
            # Press Escape to close
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(1)
            return True
        except:
            return False
    
    def close(self):
        """
        Close Chrome browser
        """
        if self.driver:
            self.driver.quit()
            logger.info("Chrome closed")

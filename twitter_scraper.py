from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv
import time

load_dotenv()

class TwitterScraper:
    def __init__(self):
        self.email = os.getenv('49uvyuvraj@gmail.com')
        self.password = os.getenv('TWITTER_PASSWORD')
        
        if not self.email or not self.password:
            raise ValueError("Twitter credentials not found in .env file")

    def setup_driver(self):
        print("Setting up Chrome driver...")
        options = webdriver.ChromeOptions()
        
        # Add required options
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        
        # Comment out headless mode for debugging
        # options.add_argument('--headless')
        
        # Create and return the driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver

    def safe_wait_and_find(self, driver, by, value, timeout=10):
        """Safely wait for and find an element with better error handling."""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"Timeout waiting for element: {value}")
            driver.save_screenshot('error.png')
            raise

    def login_twitter(self, driver):
        print(f"Attempting to log in with email: {self.email}")
        
        try:
            # Go to Twitter login page
            driver.get("https://twitter.com/i/flow/login")
            time.sleep(5)  # Wait for page load
            
            # Enter email
            print("Looking for email input...")
            email_input = self.safe_wait_and_find(
                driver,
                By.XPATH,
                "//input[@autocomplete='username']"
            )
            email_input.send_keys(self.email)
            
            # Click the 'Next' button
            print("Clicking Next...")
            next_button = self.safe_wait_and_find(
                driver,
                By.XPATH,
                "//div[@role='button']//span[text()='Next']"
            )
            next_button.click()
            time.sleep(3)
            
            # Enter password
            print("Entering password...")
            password_input = self.safe_wait_and_find(
                driver,
                By.XPATH,
                "//input[@name='password']"
            )
            password_input.send_keys(self.password)
            
            # Click the 'Log in' button
            print("Clicking Log in...")
            login_button = self.safe_wait_and_find(
                driver,
                By.XPATH,
                "//div[@role='button']//span[text()='Log in']"
            )
            login_button.click()
            time.sleep(5)
            
            # Verify login success
            try:
                self.safe_wait_and_find(
                    driver,
                    By.XPATH,
                    "//div[@data-testid='primaryColumn']"
                )
                print("Successfully logged in!")
            except TimeoutException:
                print("Failed to verify login success")
                driver.save_screenshot('login_failed.png')
                raise
                
        except Exception as e:
            print(f"Login failed with error: {str(e)}")
            driver.save_screenshot('login_error.png')
            raise

    def get_trending_topics(self):
        driver = None
        try:
            driver = self.setup_driver()
            self.login_twitter(driver)
            
            # Navigate to Explore page
            print("Navigating to Explore page...")
            driver.get("https://twitter.com/explore")
            time.sleep(5)
            
            # Find trending topics
            print("Finding trending topics...")
            trends = self.safe_wait_and_find(
                driver,
                By.CSS_SELECTOR,
                "div[aria-label='Timeline: Trending now']"
            ).find_elements(By.CSS_SELECTOR, "div[data-testid='trend']")
            
            # Extract trend texts
            trend_texts = []
            for trend in trends[:5]:
                try:
                    text = trend.find_element(By.CSS_SELECTOR, "span").text
                    trend_texts.append(text)
                except:
                    continue
            
            # Create result document
            document = {
                "_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "ip_address": "local"
            }
            
            for i, trend in enumerate(trend_texts, 1):
                document[f"nameoftrend{i}"] = trend
            
            return document
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            if driver:
                driver.save_screenshot('error.png')
            raise
            
        finally:
            if driver:
                driver.quit()

# Test the scraper
if __name__ == "__main__":
    try:
        scraper = TwitterScraper()
        results = scraper.get_trending_topics()
        print("\nSuccessfully retrieved trends:")
        for i in range(1, 6):
            print(f"{i}. {results.get(f'nameoftrend{i}', 'N/A')}")
    except Exception as e:
        print(f"Script failed: {str(e)}")
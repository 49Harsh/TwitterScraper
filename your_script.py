import time
import random
import pymongo
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# MongoDB setup (using environment variable)
MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)
db = client['twitter_trends']
collection = db['trending_topics']

# Load proxies from environment variable (split into a list)
proxies = os.getenv('PROXIES').split(',')

# Twitter credentials from .env
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

# Function to set up Selenium WebDriver with Proxy
def setup_driver(proxy):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # To run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set up proxy
    chrome_options.add_argument(f'--proxy-server={proxy}')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Function to log into Twitter and fetch trending topics
def fetch_trends():
    # Rotate proxy from the list
    proxy = random.choice(proxies)
    
    # Set up WebDriver with the chosen proxy
    driver = setup_driver(proxy)

    # Open Twitter login page
    driver.get("https://twitter.com/login")
    time.sleep(2)

    # Login to Twitter (correcting the selectors)
    try:
        username = driver.find_element(By.NAME, "session[username_or_email]")
        username.send_keys(TWITTER_USERNAME)
        username.send_keys(Keys.RETURN)
        time.sleep(2)

        password = driver.find_element(By.NAME, "session[password]")
        password.send_keys(TWITTER_PASSWORD)
        password.send_keys(Keys.RETURN)
        time.sleep(5)

        # Check if login is successful by looking for the "What's happening" section
        driver.get("https://twitter.com/i/trends")
        time.sleep(5)

        # Fetch the trending topics
        trends = driver.find_elements(By.XPATH, "//div[@aria-labelledby='trends-container']/div[2]/div")
        trend_names = [trend.text.split('\n')[0] for trend in trends[:5]]  # Get names of top 5 trends

    except Exception as e:
        print(f"Error during login or trend fetching: {e}")
        driver.quit()
        return None

    # Get current IP address used for the proxy
    ip_address = requests.get(f'http://{proxy}/ip').text

    # Store in MongoDB with a unique ID and timestamp
    record = {
        'unique_id': str(random.randint(1000000, 9999999)),
        'name_of_trend1': trend_names[0] if len(trend_names) > 0 else "N/A",
        'name_of_trend2': trend_names[1] if len(trend_names) > 1 else "N/A",
        'name_of_trend3': trend_names[2] if len(trend_names) > 2 else "N/A",
        'name_of_trend4': trend_names[3] if len(trend_names) > 3 else "N/A",
        'name_of_trend5': trend_names[4] if len(trend_names) > 4 else "N/A",
        'timestamp': datetime.now(),
        'ip_address': ip_address
    }

    # Insert into MongoDB
    collection.insert_one(record)
    
    # Close the WebDriver
    driver.quit()

    return record

# Function to generate the HTML result
def generate_html(result):
    if result:
        html_content = f"""
        <html>
            <head><title>Twitter Trending Topics</title></head>
            <body>
                <h2>These are the most happening topics as on {result['timestamp']}</h2>
                <ul>
                    <li>{result['name_of_trend1']}</li>
                    <li>{result['name_of_trend2']}</li>
                    <li>{result['name_of_trend3']}</li>
                    <li>{result['name_of_trend4']}</li>
                    <li>{result['name_of_trend5']}</li>
                </ul>
                <p>The IP address used for this query was {result['ip_address']}</p>
                <h3>Here’s a JSON extract of this record from the MongoDB:</h3>
                <pre>{result}</pre>
                <button onclick="window.location.reload();">Click here to run the query again.</button>
            </body>
        </html>
        """
    else:
        html_content = "<html><body><h2>Error occurred. Could not fetch trending topics.</h2></body></html>"
    
    return html_content

if __name__ == '__main__':
    trends_result = fetch_trends()
    print(generate_html(trends_result))

import requests
from bs4 import BeautifulSoup
import random
import logging

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.update_proxy_list()

    def update_proxy_list(self):
        """Fetch free proxies from multiple sources"""
        try:
            # Free-Proxy-List.net
            response = requests.get('https://free-proxy-list.net/')
            soup = BeautifulSoup(response.text, 'html.parser')
            proxy_list = []
            
            for row in soup.find('table').find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) > 6:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    https = cols[6].text.strip()
                    if https == 'yes':  # Only use HTTPS proxies
                        proxy_list.append(f"{ip}:{port}")
            
            self.proxies = proxy_list
            logging.info(f"Updated proxy list with {len(self.proxies)} proxies")
            
        except Exception as e:
            logging.error(f"Error updating proxy list: {str(e)}")
            raise

    def get_proxy(self):
        """Get a random proxy from the list"""
        if not self.proxies:
            self.update_proxy_list()
        
        if not self.proxies:
            raise Exception("No proxies available")
            
        proxy = random.choice(self.proxies)
        proxy_dict = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        
        return proxy, proxy_dict

    def remove_proxy(self, proxy):
        """Remove a non-working proxy from the list"""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            logging.info(f"Removed non-working proxy: {proxy}")

class TwitterScraper:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.db_client = MongoDBClient()

    def setup_driver(self, proxy):
        options = webdriver.ChromeOptions()
        options.add_argument(f'--proxy-server={proxy}')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def get_trending_topics(self):
        max_retries = 3
        retries = 0
        
        while retries < max_retries:
            try:
                proxy_ip, proxy_dict = self.proxy_manager.get_proxy()
                driver = self.setup_driver(proxy_dict['http'])
                
                try:
                    self.login_twitter(driver)
                    # Rest of your existing scraping code...
                    return document
                    
                finally:
                    driver.quit()
                    
            except Exception as e:
                logging.error(f"Error with proxy {proxy_ip}: {str(e)}")
                self.proxy_manager.remove_proxy(proxy_ip)
                retries += 1
                
        raise Exception("Failed to scrape after maximum retries")
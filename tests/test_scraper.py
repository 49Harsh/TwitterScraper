import pytest
from src.scraper import TwitterScraper
from unittest.mock import Mock, patch

@pytest.fixture
def scraper():
    return TwitterScraper()

def test_get_proxy(scraper):
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = '192.168.1.1'
        ip, proxies = scraper.get_proxy()
        assert ip == '192.168.1.1'
        assert isinstance(proxies, dict)

def test_get_trending_topics(scraper):
    with patch('selenium.webdriver.Chrome') as mock_driver:
        mock_driver.return_value.find_elements.return_value = [
            Mock(text='Trend 1\nDetails'),
            Mock(text='Trend 2\nDetails'),
            Mock(text='Trend 3\nDetails'),
            Mock(text='Trend 4\nDetails'),
            Mock(text='Trend 5\nDetails')
        ]
        result = scraper.get_trending_topics()
        assert len(result) > 0
        assert 'nameoftrend1' in result

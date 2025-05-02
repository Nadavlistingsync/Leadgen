from abc import ABC, abstractmethod
import json
import time
import random
from typing import Dict, List, Optional
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

class BaseScraper(ABC):
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.driver = None
        self.setup_selenium()

    def setup_selenium(self):
        """Setup Selenium WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={self.ua.random}')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def get_page(self, url: str, use_selenium: bool = False) -> Optional[BeautifulSoup]:
        """Get page content with appropriate delay and error handling"""
        try:
            if use_selenium:
                self.driver.get(url)
                time.sleep(random.uniform(2, 4))  # Random delay to avoid detection
                return BeautifulSoup(self.driver.page_source, 'lxml')
            else:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                time.sleep(random.uniform(1, 3))
                return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def save_leads(self, leads: List[Dict], filename: str):
        """Save leads to JSON file"""
        try:
            with open(f'src/data/{filename}', 'w') as f:
                json.dump(leads, f, indent=4)
            print(f"Saved {len(leads)} leads to {filename}")
        except Exception as e:
            print(f"Error saving leads: {str(e)}")

    def load_leads(self, filename: str) -> List[Dict]:
        """Load leads from JSON file"""
        try:
            with open(f'src/data/{filename}', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error loading leads: {str(e)}")
            return []

    @abstractmethod
    def scrape(self, *args, **kwargs) -> List[Dict]:
        """Main scraping method to be implemented by specific scrapers"""
        pass

    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()

    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup() 
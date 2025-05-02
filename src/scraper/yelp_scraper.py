from typing import Dict, List
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random

class YelpScraper(BaseScraper):
    def __init__(self, location: str = "New York, NY", business_type: str = "real estate agents"):
        super().__init__()
        self.base_url = "https://www.yelp.com"
        self.location = location
        self.business_type = business_type
        self.search_url = f"{self.base_url}/search?find_desc={business_type.replace(' ', '+')}&find_loc={location.replace(' ', '+')}"

    def extract_business_info(self, business_div: BeautifulSoup) -> Dict:
        """Extract business information from a single business div"""
        try:
            # Get business name and link
            name_elem = business_div.find('h3', class_='css-1agk4wl')
            name = name_elem.text.strip() if name_elem else None
            business_url = f"{self.base_url}{name_elem.find('a')['href']}" if name_elem and name_elem.find('a') else None

            # Get address
            address_elem = business_div.find('p', class_='css-dzq7l1')
            address = address_elem.text.strip() if address_elem else None

            # Get phone
            phone_elem = business_div.find('p', class_='css-1p9ibgf')
            phone = phone_elem.text.strip() if phone_elem else None

            # Get website
            website = None
            if business_url:
                try:
                    business_soup = self.get_page(business_url, use_selenium=True)
                    if business_soup:
                        website_elem = business_soup.find('a', class_='css-1idmmu3')
                        website = website_elem['href'] if website_elem else None
                except:
                    pass

            # Get LinkedIn profile
            linkedin = None
            if website:
                try:
                    website_soup = self.get_page(website)
                    if website_soup:
                        linkedin_link = website_soup.find('a', href=re.compile('linkedin.com'))
                        if linkedin_link:
                            linkedin = linkedin_link['href']
                except:
                    pass

            return {
                'full_name': name,
                'phone': phone,
                'website': website,
                'address': address,
                'linkedin': linkedin,
                'location': self.location,
                'source': 'yelp.com',
                'scraped_date': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error extracting business info: {str(e)}")
            return None

    def scrape(self, max_pages: int = 5) -> List[Dict]:
        """Scrape business information from Yelp"""
        leads = []
        current_page = 0

        while current_page < max_pages:
            try:
                url = f"{self.search_url}&start={current_page * 10}"
                print(f"Scraping page {current_page + 1}: {url}")
                
                soup = self.get_page(url, use_selenium=True)
                if not soup:
                    break

                business_divs = soup.find_all('div', class_='css-1qn0b6x')
                if not business_divs:
                    break

                for business_div in business_divs:
                    business_info = self.extract_business_info(business_div)
                    if business_info:
                        leads.append(business_info)
                        # Add random delay between businesses
                        time.sleep(random.uniform(1, 3))

                current_page += 1
                
                # Save progress after each page
                self.save_leads(leads, f'yelp_leads_{self.location.replace(" ", "_")}.json')

                # Add random delay between pages
                time.sleep(random.uniform(3, 5))

            except Exception as e:
                print(f"Error scraping page {current_page + 1}: {str(e)}")
                break

        return leads

if __name__ == "__main__":
    scraper = YelpScraper("New York, NY")
    leads = scraper.scrape()
    print(f"Scraped {len(leads)} leads from Yelp") 
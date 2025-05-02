from typing import Dict, List
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
from datetime import datetime

class RealtorScraper(BaseScraper):
    def __init__(self, location: str = "New York, NY"):
        super().__init__()
        self.base_url = "https://www.realtor.com"
        self.location = location
        self.search_url = f"{self.base_url}/realestateagents/{location.replace(' ', '-')}"

    def extract_agent_info(self, agent_div: BeautifulSoup) -> Dict:
        """Extract agent information from a single agent div"""
        try:
            name = agent_div.find('div', class_='agent-name').text.strip()
            phone = agent_div.find('div', class_='agent-phone').text.strip() if agent_div.find('div', class_='agent-phone') else None
            website = agent_div.find('a', class_='agent-website')['href'] if agent_div.find('a', class_='agent-website') else None
            company = agent_div.find('div', class_='agent-company').text.strip() if agent_div.find('div', class_='agent-company') else None
            
            # Try to find LinkedIn profile
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
                'company': company,
                'linkedin': linkedin,
                'location': self.location,
                'source': 'realtor.com',
                'scraped_date': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error extracting agent info: {str(e)}")
            return None

    def scrape(self, max_pages: int = 5) -> List[Dict]:
        """Scrape agent information from Realtor.com"""
        leads = []
        current_page = 1

        while current_page <= max_pages:
            try:
                url = f"{self.search_url}/pg-{current_page}"
                print(f"Scraping page {current_page}: {url}")
                
                soup = self.get_page(url, use_selenium=True)
                if not soup:
                    break

                agent_divs = soup.find_all('div', class_='agent-card')
                if not agent_divs:
                    break

                for agent_div in agent_divs:
                    agent_info = self.extract_agent_info(agent_div)
                    if agent_info:
                        leads.append(agent_info)

                current_page += 1
                
                # Save progress after each page
                self.save_leads(leads, f'realtor_leads_{self.location.replace(" ", "_")}.json')

            except Exception as e:
                print(f"Error scraping page {current_page}: {str(e)}")
                break

        return leads

if __name__ == "__main__":
    scraper = RealtorScraper("New York, NY")
    leads = scraper.scrape()
    print(f"Scraped {len(leads)} leads from Realtor.com") 
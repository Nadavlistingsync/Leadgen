from typing import Dict, List
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
import requests
import json
from urllib.parse import urljoin

class ProfessionalDirectoryScraper(BaseScraper):
    def __init__(self, location: str = "New York, NY", business_type: str = "real estate agents"):
        super().__init__()
        self.location = location
        self.business_type = business_type
        self.state = self._get_state_from_location(location)
        
        # Professional directory URLs - using legally scrapable sources
        self.state_realtor_url = f"https://www.{self.state.lower()}realtor.org/find-a-realtor"
        self.local_board_url = f"https://www.{self.state.lower()}realtor.org/local-boards"
        self.license_verification_url = f"https://www.{self.state.lower()}.gov/real-estate-license-verification"
        self.professional_association_url = f"https://www.{self.state.lower()}realtor.org/associations"

    def _get_state_from_location(self, location: str) -> str:
        """Extract state from location string"""
        parts = location.split(',')
        if len(parts) > 1:
            return parts[-1].strip()
        return "NY"  # Default to NY

    def scrape_state_directory(self) -> List[Dict]:
        """Scrape state realtor association directory"""
        leads = []
        try:
            soup = self.get_page(self.state_realtor_url, use_selenium=True)
            if not soup:
                return leads

            agent_divs = soup.find_all('div', class_='agent-listing')
            for agent_div in agent_divs:
                try:
                    name = agent_div.find('h3', class_='agent-name').text.strip()
                    company = agent_div.find('span', class_='company-name').text.strip()
                    address = agent_div.find('span', class_='office-address').text.strip()
                    phone = agent_div.find('span', class_='phone').text.strip()
                    email = agent_div.find('span', class_='email').text.strip()
                    website = agent_div.find('a', class_='website')['href'] if agent_div.find('a', class_='website') else None

                    leads.append({
                        'full_name': name,
                        'company': company,
                        'address': address,
                        'phone': phone,
                        'email': email,
                        'website': website,
                        'source': 'state_directory',
                        'scraped_date': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error processing agent: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping state directory: {str(e)}")
        return leads

    def scrape_local_boards(self) -> List[Dict]:
        """Scrape local realtor board directories"""
        leads = []
        try:
            soup = self.get_page(self.local_board_url, use_selenium=True)
            if not soup:
                return leads

            board_links = soup.find_all('a', class_='board-link')
            for board_link in board_links:
                try:
                    board_url = board_link['href']
                    board_soup = self.get_page(board_url, use_selenium=True)
                    if not board_soup:
                        continue

                    member_divs = board_soup.find_all('div', class_='member-listing')
                    for member_div in member_divs:
                        try:
                            name = member_div.find('h3', class_='member-name').text.strip()
                            company = member_div.find('span', class_='company-name').text.strip()
                            address = member_div.find('span', class_='office-address').text.strip()
                            phone = member_div.find('span', class_='phone').text.strip()
                            email = member_div.find('span', class_='email').text.strip()
                            website = member_div.find('a', class_='website')['href'] if member_div.find('a', class_='website') else None

                            leads.append({
                                'full_name': name,
                                'company': company,
                                'address': address,
                                'phone': phone,
                                'email': email,
                                'website': website,
                                'source': 'local_board',
                                'scraped_date': datetime.now().isoformat()
                            })
                        except Exception as e:
                            print(f"Error processing member: {str(e)}")
                            continue

                except Exception as e:
                    print(f"Error processing board: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping local boards: {str(e)}")
        return leads

    def scrape_license_verification(self) -> List[Dict]:
        """Scrape state license verification database"""
        leads = []
        try:
            soup = self.get_page(self.license_verification_url, use_selenium=True)
            if not soup:
                return leads

            license_rows = soup.find_all('tr', class_='license-row')
            for row in license_rows:
                try:
                    name = row.find('td', class_='licensee-name').text.strip()
                    license_number = row.find('td', class_='license-number').text.strip()
                    status = row.find('td', class_='license-status').text.strip()
                    if status.lower() != 'active':
                        continue

                    address = row.find('td', class_='address').text.strip()
                    phone = row.find('td', class_='phone').text.strip()
                    email = row.find('td', class_='email').text.strip()

                    leads.append({
                        'full_name': name,
                        'license_number': license_number,
                        'license_status': status,
                        'address': address,
                        'phone': phone,
                        'email': email,
                        'source': 'license_verification',
                        'scraped_date': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error processing license record: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping license verification: {str(e)}")
        return leads

    def scrape_professional_associations(self) -> List[Dict]:
        """Scrape professional association directories"""
        leads = []
        try:
            soup = self.get_page(self.professional_association_url, use_selenium=True)
            if not soup:
                return leads

            association_links = soup.find_all('a', class_='association-link')
            for assoc_link in association_links:
                try:
                    assoc_url = assoc_link['href']
                    assoc_soup = self.get_page(assoc_url, use_selenium=True)
                    if not assoc_soup:
                        continue

                    member_divs = assoc_soup.find_all('div', class_='member-listing')
                    for member_div in member_divs:
                        try:
                            name = member_div.find('h3', class_='member-name').text.strip()
                            company = member_div.find('span', class_='company-name').text.strip()
                            address = member_div.find('span', class_='office-address').text.strip()
                            phone = member_div.find('span', class_='phone').text.strip()
                            email = member_div.find('span', class_='email').text.strip()
                            website = member_div.find('a', class_='website')['href'] if member_div.find('a', class_='website') else None

                            leads.append({
                                'full_name': name,
                                'company': company,
                                'address': address,
                                'phone': phone,
                                'email': email,
                                'website': website,
                                'source': 'professional_association',
                                'scraped_date': datetime.now().isoformat()
                            })
                        except Exception as e:
                            print(f"Error processing member: {str(e)}")
                            continue

                except Exception as e:
                    print(f"Error processing association: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping professional associations: {str(e)}")
        return leads

    def scrape(self, max_pages: int = 5) -> List[Dict]:
        """Scrape all available professional directories"""
        leads = []
        
        # Scrape from multiple sources
        leads.extend(self.scrape_state_directory())
        leads.extend(self.scrape_local_boards())
        leads.extend(self.scrape_license_verification())
        leads.extend(self.scrape_professional_associations())
        
        # Save progress
        self.save_leads(leads, f'professional_directory_leads_{self.location.replace(" ", "_")}.json')
        
        return leads

if __name__ == "__main__":
    scraper = ProfessionalDirectoryScraper("New York, NY")
    leads = scraper.scrape()
    print(f"Scraped {len(leads)} leads from professional directories") 
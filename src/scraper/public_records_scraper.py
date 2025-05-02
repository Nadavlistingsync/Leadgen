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

class PublicRecordsScraper(BaseScraper):
    def __init__(self, location: str = "New York, NY"):
        super().__init__()
        self.location = location
        self.county = self._get_county_from_location(location)
        self.state = self._get_state_from_location(location)
        
        # Public records URLs - using government websites that allow scraping
        self.assessor_url = f"https://{self.county.lower()}.gov/assessor"
        self.business_license_url = f"https://{self.county.lower()}.gov/business-licenses"
        self.chamber_url = f"https://{self.county.lower()}chamber.org/members"
        self.county_clerk_url = f"https://{self.county.lower()}.gov/clerk"
        self.state_license_url = f"https://www.{self.state.lower()}.gov/professional-licensing"

    def _get_county_from_location(self, location: str) -> str:
        """Extract county from location string"""
        parts = location.split(',')
        if len(parts) > 1:
            return parts[0].strip().lower().replace(' ', '-')
        return "new-york"  # Default to NYC

    def _get_state_from_location(self, location: str) -> str:
        """Extract state from location string"""
        parts = location.split(',')
        if len(parts) > 1:
            return parts[-1].strip()
        return "NY"  # Default to NY

    def scrape_assessor_records(self) -> List[Dict]:
        """Scrape property assessor records from government website"""
        leads = []
        try:
            soup = self.get_page(self.assessor_url, use_selenium=True)
            if not soup:
                return leads

            # Look for property owner information
            owner_divs = soup.find_all('div', class_='property-owner')
            for owner_div in owner_divs:
                try:
                    name = owner_div.find('span', class_='owner-name').text.strip()
                    address = owner_div.find('span', class_='property-address').text.strip()
                    
                    # Get contact info if available
                    contact_div = owner_div.find('div', class_='contact-info')
                    phone = contact_div.find('span', class_='phone').text.strip() if contact_div else None
                    email = contact_div.find('span', class_='email').text.strip() if contact_div else None

                    leads.append({
                        'full_name': name,
                        'address': address,
                        'phone': phone,
                        'email': email,
                        'source': 'assessor_records',
                        'scraped_date': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error processing property owner: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping assessor records: {str(e)}")
        return leads

    def scrape_business_licenses(self) -> List[Dict]:
        """Scrape business license records from government website"""
        leads = []
        try:
            soup = self.get_page(self.business_license_url, use_selenium=True)
            if not soup:
                return leads

            business_rows = soup.find_all('tr', class_='business-row')
            for row in business_rows:
                try:
                    name = row.find('td', class_='business-name').text.strip()
                    owner = row.find('td', class_='owner-name').text.strip()
                    address = row.find('td', class_='business-address').text.strip()
                    phone = row.find('td', class_='phone').text.strip()
                    
                    leads.append({
                        'full_name': owner,
                        'business_name': name,
                        'address': address,
                        'phone': phone,
                        'source': 'business_licenses',
                        'scraped_date': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error processing business: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping business licenses: {str(e)}")
        return leads

    def scrape_county_clerk_records(self) -> List[Dict]:
        """Scrape county clerk records from government website"""
        leads = []
        try:
            soup = self.get_page(self.county_clerk_url, use_selenium=True)
            if not soup:
                return leads

            # Look for property records
            record_divs = soup.find_all('div', class_='property-record')
            for record in record_divs:
                try:
                    owner = record.find('span', class_='owner-name').text.strip()
                    address = record.find('span', class_='property-address').text.strip()
                    
                    # Get additional details if available
                    details = record.find('div', class_='property-details')
                    phone = details.find('span', class_='phone').text.strip() if details else None
                    email = details.find('span', class_='email').text.strip() if details else None

                    leads.append({
                        'full_name': owner,
                        'address': address,
                        'phone': phone,
                        'email': email,
                        'source': 'county_clerk',
                        'scraped_date': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error processing property record: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping county clerk records: {str(e)}")
        return leads

    def scrape_state_licenses(self) -> List[Dict]:
        """Scrape state professional licensing records from government website"""
        leads = []
        try:
            soup = self.get_page(self.state_license_url, use_selenium=True)
            if not soup:
                return leads

            # Look for real estate professionals
            license_rows = soup.find_all('tr', class_='license-row')
            for row in license_rows:
                try:
                    name = row.find('td', class_='licensee-name').text.strip()
                    license_type = row.find('td', class_='license-type').text.strip()
                    if 'real estate' not in license_type.lower():
                        continue
                        
                    address = row.find('td', class_='address').text.strip()
                    phone = row.find('td', class_='phone').text.strip()
                    email = row.find('td', class_='email').text.strip()

                    leads.append({
                        'full_name': name,
                        'license_type': license_type,
                        'address': address,
                        'phone': phone,
                        'email': email,
                        'source': 'state_licenses',
                        'scraped_date': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error processing license record: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping state licenses: {str(e)}")
        return leads

    def scrape_chamber_members(self) -> List[Dict]:
        """Scrape chamber of commerce member directory"""
        leads = []
        try:
            soup = self.get_page(self.chamber_url, use_selenium=True)
            if not soup:
                return leads

            member_divs = soup.find_all('div', class_='member-listing')
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
                        'source': 'chamber_of_commerce',
                        'scraped_date': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error processing member: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping chamber members: {str(e)}")
        return leads

    def scrape(self, max_pages: int = 5) -> List[Dict]:
        """Scrape all available public records"""
        leads = []
        
        # Scrape from multiple sources
        leads.extend(self.scrape_assessor_records())
        leads.extend(self.scrape_business_licenses())
        leads.extend(self.scrape_county_clerk_records())
        leads.extend(self.scrape_state_licenses())
        leads.extend(self.scrape_chamber_members())
        
        # Save progress
        self.save_leads(leads, f'public_records_leads_{self.location.replace(" ", "_")}.json')
        
        return leads

if __name__ == "__main__":
    scraper = PublicRecordsScraper("New York, NY")
    leads = scraper.scrape()
    print(f"Scraped {len(leads)} leads from public records") 
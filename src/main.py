import sys
import os
from datetime import datetime
from scraper.realtor_scraper import RealtorScraper
from config.settings import TARGET_SETTINGS, SCRAPING_SETTINGS

def main():
    try:
        # Create data directory if it doesn't exist
        os.makedirs('src/data', exist_ok=True)

        # Initialize scraper
        scraper = RealtorScraper(location=TARGET_SETTINGS['location'])
        
        # Start scraping
        print(f"Starting scraping for {TARGET_SETTINGS['location']}...")
        leads = scraper.scrape(max_pages=SCRAPING_SETTINGS['max_pages_per_source'])
        
        # Print summary
        print(f"\nScraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total leads scraped: {len(leads)}")
        
        # Save final results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        scraper.save_leads(leads, f'final_leads_{timestamp}.json')
        
    except Exception as e:
        print(f"Error in main script: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
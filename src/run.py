import os
import sys
from datetime import datetime
from scraper.yellow_pages_scraper import YellowPagesScraper
from scraper.public_records_scraper import PublicRecordsScraper
from scraper.professional_directory_scraper import ProfessionalDirectoryScraper
from utils.sheets_manager import SheetsManager
from utils.message_generator import MessageGenerator
from utils.outreach_manager import OutreachManager
from config.settings import TARGET_SETTINGS, SCRAPING_SETTINGS
import json

def main():
    try:
        # Create necessary directories
        os.makedirs('src/data', exist_ok=True)
        
        # Initialize components
        sheets_manager = SheetsManager()
        message_generator = MessageGenerator()
        outreach_manager = OutreachManager()
        
        # Step 1: Scrape leads from multiple sources
        print("Starting lead scraping...")
        all_leads = []
        
        # Scrape from Yellow Pages
        print("Scraping from Yellow Pages...")
        yp_scraper = YellowPagesScraper(
            location=TARGET_SETTINGS['location'],
            business_type="real estate agents"
        )
        yp_leads = yp_scraper.scrape(max_pages=SCRAPING_SETTINGS['max_pages_per_source'])
        all_leads.extend(yp_leads)
        print(f"Scraped {len(yp_leads)} leads from Yellow Pages")
        
        # Scrape from Public Records
        print("Scraping from Public Records...")
        pr_scraper = PublicRecordsScraper(
            location=TARGET_SETTINGS['location']
        )
        pr_leads = pr_scraper.scrape(max_pages=SCRAPING_SETTINGS['max_pages_per_source'])
        all_leads.extend(pr_leads)
        print(f"Scraped {len(pr_leads)} leads from Public Records")
        
        # Scrape from Professional Directories
        print("Scraping from Professional Directories...")
        pd_scraper = ProfessionalDirectoryScraper(
            location=TARGET_SETTINGS['location'],
            business_type="real estate agents"
        )
        pd_leads = pd_scraper.scrape(max_pages=SCRAPING_SETTINGS['max_pages_per_source'])
        all_leads.extend(pd_leads)
        print(f"Scraped {len(pd_leads)} leads from Professional Directories")
        
        print(f"Total leads scraped: {len(all_leads)}")
        
        # Step 2: Save to Google Sheets
        print("Saving leads to Google Sheets...")
        sheets_manager.append_leads(all_leads)
        
        # Step 3: Generate and send messages
        print("Generating and sending messages...")
        for lead in all_leads:
            try:
                # Generate messages
                messages = message_generator.generate_messages(lead)
                
                # Send outreach
                results = outreach_manager.process_lead(lead, messages)
                
                # Update lead status
                status = "Contacted" if any(results.values()) else "Failed"
                sheets_manager.update_lead_status(
                    lead.get('id', ''),
                    status,
                    json.dumps(results)
                )
                
                print(f"Processed lead: {lead.get('full_name', 'Unknown')}")
                
            except Exception as e:
                print(f"Error processing lead: {str(e)}")
                continue
        
        print("\nProcess completed successfully!")
        print(f"Total leads processed: {len(all_leads)}")
        
    except Exception as e:
        print(f"Error in main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
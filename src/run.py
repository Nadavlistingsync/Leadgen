import os
import sys
from datetime import datetime
from scraper.realtor_scraper import RealtorScraper
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
        
        # Step 1: Scrape leads
        print("Starting lead scraping...")
        scraper = RealtorScraper(location=TARGET_SETTINGS['location'])
        leads = scraper.scrape(max_pages=SCRAPING_SETTINGS['max_pages_per_source'])
        print(f"Scraped {len(leads)} leads")
        
        # Step 2: Save to Google Sheets
        print("Saving leads to Google Sheets...")
        sheets_manager.append_leads(leads)
        
        # Step 3: Generate and send messages
        print("Generating and sending messages...")
        for lead in leads:
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
        print(f"Total leads processed: {len(leads)}")
        
    except Exception as e:
        print(f"Error in main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
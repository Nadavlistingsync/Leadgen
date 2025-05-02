from typing import List, Dict
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from config.settings import STORAGE_SETTINGS
from datetime import datetime

class SheetsManager:
    def __init__(self):
        self.creds = None
        self.sheet_id = STORAGE_SETTINGS['google_sheet_id']
        self.credentials_path = STORAGE_SETTINGS['google_sheets_credentials']
        self.service = None
        self.setup_credentials()

    def setup_credentials(self):
        """Setup Google Sheets API credentials"""
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('sheets', 'v4', credentials=self.creds)

    def create_sheet(self, title: str = "Leads Database"):
        """Create a new Google Sheet"""
        spreadsheet = {
            'properties': {
                'title': title
            },
            'sheets': [{
                'properties': {
                    'title': 'Leads',
                    'gridProperties': {
                        'rowCount': 1000,
                        'columnCount': 26
                    }
                }
            }]
        }
        
        spreadsheet = self.service.spreadsheets().create(body=spreadsheet).execute()
        self.sheet_id = spreadsheet['spreadsheetId']
        
        # Set up headers
        headers = [
            'Full Name', 'Email', 'Phone', 'LinkedIn', 'Website', 'Company',
            'Location', 'Source', 'Scraped Date', 'Status', 'Last Contact',
            'Email Sent', 'LinkedIn Sent', 'SMS Sent', 'Response',
            'Follow-up Count', 'Next Follow-up', 'Notes'
        ]
        self.update_sheet([headers], 'A1:R1')
        
        return self.sheet_id

    def update_sheet(self, data: List[List], range_name: str):
        """Update sheet with new data"""
        body = {
            'values': data
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        return result

    def append_leads(self, leads: List[Dict]):
        """Append new leads to the sheet"""
        values = []
        for lead in leads:
            row = [
                lead.get('full_name', ''),
                lead.get('email', ''),
                lead.get('phone', ''),
                lead.get('linkedin', ''),
                lead.get('website', ''),
                lead.get('company', ''),
                lead.get('location', ''),
                lead.get('source', ''),
                lead.get('scraped_date', ''),
                'New',  # Status
                '',  # Last Contact
                'No',  # Email Sent
                'No',  # LinkedIn Sent
                'No',  # SMS Sent
                '',  # Response
                0,  # Follow-up Count
                '',  # Next Follow-up
                ''  # Notes
            ]
            values.append(row)
        
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range='Leads!A:R',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        return result

    def update_lead_status(self, row_index: int, status: str, notes: str = ''):
        """Update lead status and notes"""
        range_name = f'Leads!J{row_index}:R{row_index}'
        values = [[
            status,  # Status
            datetime.now().isoformat(),  # Last Contact
            '',  # Email Sent (will be updated separately)
            '',  # LinkedIn Sent (will be updated separately)
            '',  # SMS Sent (will be updated separately)
            '',  # Response
            0,  # Follow-up Count
            '',  # Next Follow-up
            notes  # Notes
        ]]
        return self.update_sheet(values, range_name)

    def get_all_leads(self) -> List[Dict]:
        """Get all leads from the sheet"""
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range='Leads!A:R'
        ).execute()
        
        values = result.get('values', [])
        if not values:
            return []
        
        headers = values[0]
        leads = []
        for row in values[1:]:
            lead = dict(zip(headers, row))
            leads.append(lead)
        
        return leads 